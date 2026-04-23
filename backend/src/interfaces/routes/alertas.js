const { Router } = require('express');
const { AlertaService, KpiService } = require('../../application/services');
const { authMiddleware } = require('../middleware/auth');
const router = Router();

/**
 * @swagger
 * /api/alertas:
 *   get:
 *     summary: Listar alertas
 *     tags: [Alertas]
 *     security: [{ bearerAuth: [] }]
 *     parameters:
 *       - in: query
 *         name: resolvido
 *         schema: { type: boolean }
 *       - in: query
 *         name: tipo
 *         schema: { type: string, enum: [URGENTE, ATENCAO, PENDENTE] }
 *     responses:
 *       200: { description: Lista de alertas }
 *       401: { description: Não autorizado }
 */
router.get('/', authMiddleware, (req, res, next) => {
  try {
    const filtros = {};
    if (req.query.resolvido !== undefined) filtros.resolvido = req.query.resolvido === 'true';
    if (req.query.tipo) filtros.tipo = req.query.tipo;
    res.json(AlertaService.listar(filtros));
  } catch (err) { next(err); }
});

/**
 * @swagger
 * /api/alertas/{id}/resolver:
 *   patch:
 *     summary: Marcar alerta como resolvido
 *     tags: [Alertas]
 *     security: [{ bearerAuth: [] }]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema: { type: integer }
 *     responses:
 *       200: { description: Resolvido }
 *       404: { description: Não encontrado }
 */
router.patch('/:id/resolver', authMiddleware, (req, res, next) => {
  try {
    res.json(AlertaService.resolver(Number(req.params.id)));
  } catch (err) { next(err); }
});

/**
 * @swagger
 * /api/alertas:
 *   post:
 *     summary: Criar novo alerta
 *     tags: [Alertas]
 *     security: [{ bearerAuth: [] }]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [tipo, titulo, ala]
 *             properties:
 *               tipo: { type: string, enum: [URGENTE, ATENCAO, PENDENTE] }
 *               titulo: { type: string }
 *               descricao: { type: string }
 *               prazo: { type: string }
 *               ala: { type: string }
 *               prioridade: { type: integer, minimum: 1, maximum: 3 }
 *     responses:
 *       201: { description: Criado }
 */
router.post('/', authMiddleware, (req, res, next) => {
  try {
    const result = AlertaService.criar(req.body);
    res.status(201).json({ id: result.lastInsertRowid, message: 'Alerta criado' });
  } catch (err) { next(err); }
});

/**
 * @swagger
 * /api/kpis:
 *   get:
 *     summary: KPIs do dashboard
 *     tags: [KPIs]
 *     security: [{ bearerAuth: [] }]
 *     responses:
 *       200: { description: KPIs atuais }
 */
router.get('/kpis', authMiddleware, (req, res, next) => {
  try {
    res.json(KpiService.get());
  } catch (err) { next(err); }
});

module.exports = router;
