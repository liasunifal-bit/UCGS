const { Router } = require('express');
const { MapaService } = require('../../application/services');
const { authMiddleware } = require('../middleware/auth');
const router = Router();

/**
 * @swagger
 * /api/mapas:
 *   get:
 *     summary: Listar mapas de risco
 *     tags: [Mapas de Risco]
 *     security: [{ bearerAuth: [] }]
 *     responses:
 *       200: { description: Lista de mapas }
 */
router.get('/', authMiddleware, (req, res, next) => {
  try { res.json(MapaService.listar()); } catch (err) { next(err); }
});

/**
 * @swagger
 * /api/mapas/{id}:
 *   put:
 *     summary: Atualizar mapa de risco
 *     tags: [Mapas de Risco]
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
 *             properties:
 *               status: { type: string, enum: [Atualizado, Vencido, Pendente] }
 *               dataAtualizacao: { type: string }
 *               totalRiscos: { type: integer }
 *               criticos: { type: integer }
 *     responses:
 *       200: { description: Atualizado }
 *       404: { description: Não encontrado }
 */
router.put('/:id', authMiddleware, (req, res, next) => {
  try {
    res.json(MapaService.atualizar(Number(req.params.id), req.body));
  } catch (err) { next(err); }
});

module.exports = router;
