const { Router } = require('express');
const { VacinaService } = require('../../application/services');
const { authMiddleware } = require('../middleware/auth');
const router = Router();

/**
 * @swagger
 * /api/vacinas:
 *   get:
 *     summary: Listar controle de vacinas
 *     tags: [Vacinas]
 *     security: [{ bearerAuth: [] }]
 *     responses:
 *       200: { description: Lista de vacinas }
 */
router.get('/', authMiddleware, (req, res, next) => {
  try { res.json(VacinaService.listar()); } catch (err) { next(err); }
});

/**
 * @swagger
 * /api/vacinas/{id}:
 *   put:
 *     summary: Atualizar dados de vacina
 *     tags: [Vacinas]
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
 *               aplicadas: { type: integer }
 *               pendentes: { type: integer }
 *               estoque: { type: integer }
 *     responses:
 *       200: { description: Atualizado }
 *       404: { description: Não encontrado }
 */
router.put('/:id', authMiddleware, (req, res, next) => {
  try {
    res.json(VacinaService.atualizar(Number(req.params.id), req.body));
  } catch (err) { next(err); }
});

module.exports = router;
