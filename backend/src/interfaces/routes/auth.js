const { Router } = require('express');
const { AuthService } = require('../../application/services');
const router = Router();

/**
 * @swagger
 * /api/auth/login:
 *   post:
 *     summary: Login e geração de token JWT
 *     tags: [Auth]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               email: { type: string, example: "admin@sst.gov" }
 *               password: { type: string, example: "admin123" }
 *     responses:
 *       200:
 *         description: Token JWT gerado
 *       401:
 *         description: Credenciais inválidas
 */
router.post('/login', async (req, res, next) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ error: 'email e password são obrigatórios' });
    }
    const resultado = await AuthService.login(email, password);
    res.json(resultado);
  } catch (err) { next(err); }
});

module.exports = router;
