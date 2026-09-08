<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Carita feliz</title>
</head>
<body>

<canvas id="canvas" width="500" height="500"></canvas>

<script>
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Fondo blanco
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

// Cara amarilla
ctx.fillStyle = "yellow";
ctx.beginPath();
ctx.arc(250, 250, 150, 0, Math.PI * 2);
ctx.fill();

// Ojos
ctx.fillStyle = "black";
ctx.beginPath();
ctx.arc(200, 210, 15, 0, Math.PI * 2);
ctx.arc(300, 210, 15, 0, Math.PI * 2);
ctx.fill();

// Sonrisa
ctx.beginPath();
ctx.arc(250, 250, 80, 0, Math.PI);
ctx.lineWidth = 8;
ctx.stroke();
</script>

</body>
</html>