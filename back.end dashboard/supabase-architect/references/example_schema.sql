-- ============================================================
-- SUPABASE ARCHITECT — Reference Schema (Multi-tenant SaaS)
-- ============================================================
-- Purpose: Demonstrates best-practice structure for a SaaS app
-- with organizations, users, roles, content, files, and audit.
-- ============================================================

-- ──────────────────────────────────────────────────
-- 1. ORGANIZATIONS (tenants)
-- ──────────────────────────────────────────────────
CREATE TABLE public.organizations (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  slug        TEXT UNIQUE NOT NULL,
  plan        TEXT DEFAULT 'free' CHECK (plan IN ('free', 'pro', 'enterprise')),
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.organizations ENABLE ROW LEVEL SECURITY;

-- ──────────────────────────────────────────────────
-- 2. PROFILES (mirrors auth.users — NEVER expose auth.users directly)
-- ──────────────────────────────────────────────────
CREATE TABLE public.profiles (
  id           UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  org_id       UUID REFERENCES public.organizations(id) ON DELETE SET NULL,
  username     TEXT UNIQUE,
  full_name    TEXT,
  avatar_url   TEXT,
  role         TEXT DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
  is_active    BOOLEAN DEFAULT TRUE,
  created_at   TIMESTAMPTZ DEFAULT NOW(),
  updated_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_profiles_org ON public.profiles(org_id);
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Auto-create profile on user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, avatar_url)
  VALUES (
    NEW.id,
    NEW.raw_user_meta_data->>'full_name',
    NEW.raw_user_meta_data->>'avatar_url'
  );
  RETURN NEW;
END;
$$;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ──────────────────────────────────────────────────
-- 3. CONTENT (generic — replace with your domain entity)
-- ──────────────────────────────────────────────────
CREATE TABLE public.content (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id       UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  owner_id     UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  title        TEXT NOT NULL,
  body         TEXT,
  status       TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
  metadata     JSONB DEFAULT '{}',
  created_at   TIMESTAMPTZ DEFAULT NOW(),
  updated_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_content_org   ON public.content(org_id);
CREATE INDEX idx_content_owner ON public.content(owner_id);
CREATE INDEX idx_content_status ON public.content(status);
ALTER TABLE public.content ENABLE ROW LEVEL SECURITY;

-- ──────────────────────────────────────────────────
-- 4. FILE REFERENCES (metadata — actual files live in storage)
-- ──────────────────────────────────────────────────
CREATE TABLE public.file_refs (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id       UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  uploaded_by  UUID NOT NULL REFERENCES public.profiles(id),
  content_id   UUID REFERENCES public.content(id) ON DELETE SET NULL,
  bucket       TEXT NOT NULL,
  path         TEXT NOT NULL,
  mime_type    TEXT,
  size_bytes   BIGINT,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_file_refs_org  ON public.file_refs(org_id);
CREATE INDEX idx_file_refs_content ON public.file_refs(content_id);
ALTER TABLE public.file_refs ENABLE ROW LEVEL SECURITY;

-- ──────────────────────────────────────────────────
-- 5. AUDIT LOG
-- ──────────────────────────────────────────────────
CREATE TABLE public.audit_log (
  id           BIGSERIAL PRIMARY KEY,
  table_name   TEXT NOT NULL,
  operation    TEXT NOT NULL CHECK (operation IN ('INSERT', 'UPDATE', 'DELETE')),
  record_id    UUID,
  old_data     JSONB,
  new_data     JSONB,
  changed_by   UUID REFERENCES auth.users(id),
  changed_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_table   ON public.audit_log(table_name);
CREATE INDEX idx_audit_record  ON public.audit_log(record_id);
CREATE INDEX idx_audit_changed ON public.audit_log(changed_at DESC);
-- Note: Do NOT enable RLS on audit_log if only admins should access it —
-- restrict via service_role in Edge Functions instead.

-- Reusable audit trigger function
CREATE OR REPLACE FUNCTION public.audit_trigger_fn()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  INSERT INTO public.audit_log(table_name, operation, record_id, old_data, new_data, changed_by)
  VALUES (
    TG_TABLE_NAME,
    TG_OP,
    COALESCE(NEW.id, OLD.id),
    CASE WHEN TG_OP IN ('DELETE', 'UPDATE') THEN to_jsonb(OLD) END,
    CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) END,
    auth.uid()
  );
  RETURN COALESCE(NEW, OLD);
END;
$$;

-- Apply audit trigger to content table
CREATE TRIGGER audit_content
  AFTER INSERT OR UPDATE OR DELETE ON public.content
  FOR EACH ROW EXECUTE FUNCTION public.audit_trigger_fn();

-- ──────────────────────────────────────────────────
-- 6. UPDATED_AT HELPER
-- ──────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

CREATE TRIGGER set_profiles_updated_at  BEFORE UPDATE ON public.profiles  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();
CREATE TRIGGER set_orgs_updated_at      BEFORE UPDATE ON public.organizations FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();
CREATE TRIGGER set_content_updated_at   BEFORE UPDATE ON public.content    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

-- ──────────────────────────────────────────────────
-- 7. RLS POLICIES
-- ──────────────────────────────────────────────────

-- Helper: get current user's org_id
CREATE OR REPLACE FUNCTION public.current_user_org()
RETURNS UUID LANGUAGE sql STABLE AS $$
  SELECT org_id FROM public.profiles WHERE id = auth.uid();
$$;

-- Helper: check if current user is admin or owner
CREATE OR REPLACE FUNCTION public.is_org_admin()
RETURNS BOOLEAN LANGUAGE sql STABLE AS $$
  SELECT role IN ('owner', 'admin')
  FROM public.profiles WHERE id = auth.uid();
$$;

-- PROFILES policies
CREATE POLICY "profiles: users see own org members"
  ON public.profiles FOR SELECT
  USING (org_id = public.current_user_org());

CREATE POLICY "profiles: users update own profile"
  ON public.profiles FOR UPDATE
  USING (id = auth.uid());

-- ORGANIZATIONS policies
CREATE POLICY "orgs: members can read own org"
  ON public.organizations FOR SELECT
  USING (id = public.current_user_org());

CREATE POLICY "orgs: owners can update"
  ON public.organizations FOR UPDATE
  USING (
    id = public.current_user_org() AND public.is_org_admin()
  );

-- CONTENT policies
CREATE POLICY "content: org members can read published"
  ON public.content FOR SELECT
  USING (
    org_id = public.current_user_org() AND
    (status = 'published' OR owner_id = auth.uid() OR public.is_org_admin())
  );

CREATE POLICY "content: members can insert into own org"
  ON public.content FOR INSERT
  WITH CHECK (
    org_id = public.current_user_org() AND
    owner_id = auth.uid()
  );

CREATE POLICY "content: owner or admin can update"
  ON public.content FOR UPDATE
  USING (
    org_id = public.current_user_org() AND
    (owner_id = auth.uid() OR public.is_org_admin())
  );

CREATE POLICY "content: owner or admin can delete"
  ON public.content FOR DELETE
  USING (
    org_id = public.current_user_org() AND
    (owner_id = auth.uid() OR public.is_org_admin())
  );

-- FILE_REFS policies (mirrors content access)
CREATE POLICY "file_refs: org members can read"
  ON public.file_refs FOR SELECT
  USING (org_id = public.current_user_org());

CREATE POLICY "file_refs: authenticated can insert into own org"
  ON public.file_refs FOR INSERT
  WITH CHECK (
    org_id = public.current_user_org() AND
    uploaded_by = auth.uid()
  );

-- ──────────────────────────────────────────────────
-- 8. STORAGE BUCKET POLICIES
-- ──────────────────────────────────────────────────
-- Run these in the Supabase Dashboard or via SQL editor:

-- INSERT INTO storage.buckets (id, name, public) VALUES ('org-files', 'org-files', false);

-- Storage: allow org members to access own org folder
-- CREATE POLICY "storage: org members access own folder"
--   ON storage.objects FOR ALL
--   USING (
--     bucket_id = 'org-files' AND
--     (storage.foldername(name))[1] = public.current_user_org()::TEXT
--   );
