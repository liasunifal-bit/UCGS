
import os

def fix_index_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Fix emoji mojibake
        content = content.replace("'ðŸ’¡'", "'💡'")
        
        # Fix script order
        # We look for the specific block and rewrite it
        old_block_start = "<!-- Supabase SDK + Auth Handlers -->"
        old_block_end = "});\n\n\n\n  </script>" # This is tricky due to newlines
        
        # Let's use a more robust regex-like replacement for the script
        import re
        
        # Pattern to find the whole Supabase script section including the faulty onload and the definition below it
        pattern = re.compile(r'<!-- Supabase SDK \+ Auth Handlers -->.*?function initSupabase\(\).*?document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{.*?if \(typeof supabase !== \'undefined\' && !window\._supa\) \{.*?initSupabase\(\);.*?\} \);\s*<\/script>', re.DOTALL)
        
        new_script = """<!-- Supabase SDK + Auth Handlers -->
  <script>
  function initSupabase() {
    try {
      window._supa = supabase.createClient(
        'https://llqphjlpypnyvknpfdyn.supabase.co',
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow'
      );
      console.log('[UCGS] Supabase client initialized:', !!window._supa);

      window._supa.auth.onAuthStateChange(function(event, session) {
        console.log('[UCGS] Auth event:', event, !!session);
        var overlay = document.getElementById('authOverlay');
        if (session && overlay) {
          overlay.style.transition = 'opacity 0.5s';
          overlay.style.opacity = '0';
          setTimeout(function() { overlay.style.display = 'none'; }, 500);
        }
      });

      if (typeof PacientesServiceFactory === 'function') {
        window.PacientesService = PacientesServiceFactory(window._supa);
      }
    } catch(e) {
      console.error('[UCGS] Failed to initialize Supabase:', e);
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    if (typeof supabase !== 'undefined' && !window._supa) {
      initSupabase();
    }
  });
  </script>
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2" onload="initSupabase()" onerror="console.error('Supabase CDN failed to load')"></script>"""
        
        # If regex fails, we'll try a simpler approach
        match = pattern.search(content)
        if match:
            content = content[:match.start()] + new_script + content[match.end():]
            print("Successfully replaced Supabase script block using regex.")
        else:
            print("Regex match failed, trying simpler replacement...")
            # Simple fallback for the most critical part
            content = content.replace('src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2" onload="initSupabase()"', 'src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"')
            # We still need to ensure initSupabase is defined. But it IS defined below.
            # The real issue was the onload firing before definition.
            # Removing onload and letting DOMContentLoaded handle it is a safe fix.
            print("Simplified fix: removed onload from script tag.")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("File updated successfully.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_index_html(r"c:\Users\maria\Downloads\antigravity lias\dashboard\index.html")
