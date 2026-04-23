const { Router } = require('express');
const { ProtocoloService } = require('../../application/services');
const { authMiddleware } = require('../middleware/auth');
const router = Router();

/**
 * @swagger
 * /api/protocolos:
 *   get:
 *     summary: Listar protocolos de segurança
 *     tags: [Protocolos]
 *     security: [{ bearerAuth: [] }]
 *     responses:
 *       200: { description: Lista de protocolos }
 */
router.get('/', authMiddleware, (req, res, next) => {
  try { res.json(ProtocoloService.listar()); } catch (err) { next(err); }
});

/**
 * @swagger
 * /api/protocolos/{id}:
 *   put:
 *     summary: Atualizar protocolo
 *     tags: [Protocolos]
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
 *               revisados: { type: integer }
 *               pendentes: { type: integer }
 *               observacao: { type: string }
 *     responses:
 *       200: { description: Atualizado }
 *       404: { description: Não encontrado }
 */
router.put('/:id', authMiddleware, (req, res, next) => {
  try {
    res.json(ProtocoloService.atualizar(Number(req.params.id), req.body));
  } catch (err) { next(err); }
});

module.exports = router;
