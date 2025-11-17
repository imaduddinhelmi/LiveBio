function requireAuth(req, res, next) {
  if (!req.session || !req.session.authenticated) {
    return res.status(401).json({ 
      success: false, 
      error: 'Authentication required' 
    });
  }
  next();
}

function checkAuthOptional(req, res, next) {
  req.isAuthenticated = !!(req.session && req.session.authenticated);
  next();
}

module.exports = { requireAuth, checkAuthOptional };
