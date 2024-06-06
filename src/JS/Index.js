const express = require("express");

const app= express();

const port= process.env.PORT || 3000;

app.get("/",(req, res)=>{
    const htmlResponse=`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE-edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/src/CSS/disenioFinalEncuesta.css">
            <title>Document</title>
        </head>
        </head>
        <body>
        <div class="thank-you-container">
            <h1>¡Gracias por su Participación!</h1>
            <p>Apreciamos mucho el tiempo que ha dedicado a completar nuestra encuesta. Sus respuestas son muy valiosas para nosotros y nos ayudarán a mejorar nuestros servicios.</p>
            <p>Si tiene alguna pregunta o necesita más información, no dude en ponerse en contacto con nosotros.</p>
        </div>
        </body>
        </html>
    `;
    res.send(htmlResponse);
});

app.listen(port,()=>{
    console.log(`port runing in http://localhost:${port}`);
});