var express = require("express");
var app = express();

const FLAG = process.env.FLAG;
const PORT = process.env.PORT;

app.get("/", (req, res, next) => {
    return res.send('FLAG をどうぞ: <a href="/flag">/flag</a>');
});

const check = (req, res, next) => {
    if (!req.headers['x-ctf4b-request'] || req.headers['x-ctf4b-request'] !== 'ctf4b') {
        return res.status(403).send('403 Forbidden');
    }

    next();
}

app.get("/flag", check, (req, res, next) => {
    return res.send(FLAG);
})

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});