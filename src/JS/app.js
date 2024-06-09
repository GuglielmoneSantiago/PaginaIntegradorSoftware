const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to serve static files
app.use(express.static('public'));

// Route to get survey results
app.get('/api/results', (req, res) => {
    const surveyResults = require("./src/surve");
    res.json(surveyResults);
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});