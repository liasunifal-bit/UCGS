const { Router } = require('express');
const { AcidenteService } = require('../../application/services');
const { authMiddleware } = require('../middleware/auth');
const router = Router();

/**
 * @swagger
 * /api/acidentes:
 *   get:
 *     summary: Listar acidentes de trabalho
 *     tags: [Acidentes]
 *     security: [{ bearerAuth: [] }]
 *     parameters:
 *       - in: query
 *         name: gravidade
 *         schema: { type: string, enum: [Leve, Moderado, Grave] }
 *     responses:
 *       200: { description: Lista de acidentes }
 */
router.get('/', authMiddleware, (req, res, next) => {
  try {
    res.json(AcidenteService.listar(req.query.gravidade ? { gravidade: req.query.gravidade } : {}));
  } catch (err) { next(err); }
});

/**
 * @swagger
 * /api/acidentes:
 *   post:
 *     summary: Registrar novo acidente
 *     tags: [Acidentes]
 *     security: [{ bearerAuth: [] }]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [data, tipo]
 *             properties:
 *               data: { type: string, example: "2026-03-21" }
 *               tipo: { type: string, example: "Queda" }
 *               envolvido: { type: string }
 *               descricao: { type: string }
 *               gravidade: { type: string, enum: [Leve, Moderado, Grave] }
 *               ala: { type: string }
 *     responses:
 *       201: { description: Registrado }
 */
router.post('/', authMiddleware, (req, res, next) => {
  try {
    const acidente = AcidenteService.registrar(req.body);
    res.status(201).json(acidente);
  } catch (err) { next(err); }
});

module.exports = router;
