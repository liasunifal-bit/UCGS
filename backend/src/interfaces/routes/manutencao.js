const { Router } = require('express');
const { ManutencaoService } = require('../../application/services');
const { authMiddleware } = require('../middleware/auth');
const router = Router();

/**
 * @swagger
 * /api/manutencao:
 *   get:
 *     summary: Listar manutenções
 *     tags: [Manutenção]
 *     security: [{ bearerAuth: [] }]
 *     parameters:
 *       - in: query
 *         name: status
 *         schema: { type: string, enum: [Em dia, Atrasado] }
 *     responses:
 *       200: { description: Lista de manutenções }
 */
router.get('/', authMiddleware, (req, res, next) => {
  try {
    res.json(ManutencaoService.listar(req.query.status ? { status: req.query.status } : {}));
  } catch (err) { next(err); }
});

/**
 * @swagger
 * /api/manutencao/{id}/executar:
 *   patch:
 *     summary: Registrar execução de manutenção
 *     tags: [Manutenção]
 *     security: [{ bearerAuth: [] }]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema: { type: integer }
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [dataRealizada, proximaData]
 *             properties:
 *               dataRealizada: { type: string, example: "2026-03-21" }
 *               proximaData: { type: string, example: "2026-09-21" }
 *     responses:
 *       200: { description: Atualizado }
 *       404: { description: Não encontrado }
 */
router.patch('/:id/executar', authMiddleware, (req, res, next) => {
  try {
    res.json(ManutencaoService.executar(Number(req.params.id), req.body));
  } catch (err) { next(err); }
});

module.exports = router;
