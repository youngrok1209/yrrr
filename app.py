import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="벽돌깨기 게임", page_icon="🎮", layout="centered")

st.title("🎮 Classic Breakout Game")
st.caption("방향키(←, →) 또는 마우스를 움직여 패들을 조작하세요.")

# HTML/JavaScript 기반 벽돌깨기 게임 코드
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        * { padding: 0; margin: 0; }
        body { background: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; }
        canvas { background: #1e222d; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    </style>
</head>
<body>

<canvas id="myCanvas" width="480" height="320"></canvas>

<script>
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");

    // 공 설정
    let x = canvas.width / 2;
    let y = canvas.height - 30;
    let dx = 3;
    let dy = -3;
    const ballRadius = 8;

    // 패들 설정
    const paddleHeight = 10;
    const paddleWidth = 75;
    let paddleX = (canvas.width - paddleWidth) / 2;
    let rightPressed = false;
    let leftPressed = false;

    // 벽돌 설정
    const brickRowCount = 3;
    const brickColumnCount = 5;
    const brickWidth = 75;
    const brickHeight = 18;
    const brickPadding = 10;
    const brickOffsetTop = 30;
    const brickOffsetLeft = 30;

    // 점수 및 상태
    let score = 0;
    let gameOver = false;
    let gameWon = false;

    const bricks = [];
    for (let c = 0; c < brickColumnCount; c++) {
        bricks[c] = [];
        for (let r = 0; r < brickRowCount; r++) {
            bricks[c][r] = { x: 0, y: 0, status: 1 };
        }
    }

    // 키보드 & 마우스 이벤트
    document.addEventListener("keydown", keyDownHandler, false);
    document.addEventListener("keyup", keyUpHandler, false);
    document.addEventListener("mousemove", mouseMoveHandler, false);

    function keyDownHandler(e) {
        if (e.key === "Right" || e.key === "ArrowRight") rightPressed = true;
        else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = true;
    }

    function keyUpHandler(e) {
        if (e.key === "Right" || e.key === "ArrowRight") rightPressed = false;
        else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = false;
    }

    function mouseMoveHandler(e) {
        const relativeX = e.clientX - canvas.offsetLeft;
        if (relativeX > 0 && relativeX < canvas.width) {
            paddleX = relativeX - paddleWidth / 2;
        }
    }

    // 충돌 감지
    function collisionDetection() {
        for (let c = 0; c < brickColumnCount; c++) {
            for (let r = 0; r < brickRowCount; r++) {
                const b = bricks[c][r];
                if (b.status === 1) {
                    if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
                        dy = -dy;
                        b.status = 0;
                        score++;
                        if (score === brickRowCount * brickColumnCount) {
                            gameWon = true;
                        }
                    }
                }
            }
        }
    }

    function drawBall() {
        ctx.beginPath();
        ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
        ctx.fillStyle = "#FF4B4B";
        ctx.fill();
        ctx.closePath();
    }

    function drawPaddle() {
        ctx.beginPath();
        ctx.rect(paddleX, canvas.height - paddleHeight - 5, paddleWidth, paddleHeight);
        ctx.fillStyle = "#00CC96";
        ctx.fill();
        ctx.closePath();
    }

    function drawBricks() {
        const colors = ["#636EFA", "#EF553B", "#00CC96"];
        for (let c = 0; c < brickColumnCount; c++) {
            for (let r = 0; r < brickRowCount; r++) {
                if (bricks[c][r].status === 1) {
                    const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                    const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                    bricks[c][r].x = brickX;
                    bricks[c][r].y = brickY;
                    ctx.beginPath();
                    ctx.rect(brickX, brickY, brickWidth, brickHeight);
                    ctx.fillStyle = colors[r % colors.length];
                    ctx.fill();
                    ctx.closePath();
                }
            }
        }
    }

    function drawScore() {
        ctx.font = "14px sans-serif";
        ctx.fillStyle = "#FFFFFF";
        ctx.fillText("Score: " + score, 8, 20);
    }

    function drawMessage(text, color) {
        ctx.font = "bold 24px sans-serif";
        ctx.fillStyle = color;
        ctx.textAlign = "center";
        ctx.fillText(text, canvas.width / 2, canvas.height / 2);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBricks();
        drawBall();
        drawPaddle();
        drawScore();
        collisionDetection();

        if (gameWon) {
            drawMessage("YOU WIN! 🎉", "#00CC96");
            return;
        }

        if (gameOver) {
            drawMessage("GAME OVER 💥", "#FF4B4B");
            return;
        }

        // 벽 반사 (좌/우)
        if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
            dx = -dx;
        }

        // 천장 반사
        if (y + dy < ballRadius) {
            dy = -dy;
        } else if (y + dy > canvas.height - ballRadius - 5) {
            // 패들 충돌
            if (x > paddleX && x < paddleX + paddleWidth) {
                dy = -dy;
            } else if (y + dy > canvas.width) {
                gameOver = true;
            }
        }

        // 패들 이동
        if (rightPressed && paddleX < canvas.width - paddleWidth) {
            paddleX += 5;
        } else if (leftPressed && paddleX > 0) {
            paddleX -= 5;
        }

        x += dx;
        y += dy;

        requestAnimationFrame(draw);
    }

    draw();
</script>
</body>
</html>
"""

# HTML 컴포넌트 렌더링
components.html(game_html, height=360)

st.markdown("---")
st.markdown("💡 **팁**: 다시 시작하려면 페이지를 새로고침(F5)하세요.")
