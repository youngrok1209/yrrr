import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="벽돌깨기 게임 Pro", page_icon="🎮", layout="centered")

st.title("🎮 Breakout Game: Item & Stages")
st.caption("방향키(←, →) 또는 마우스를 움직여 패들을 조작하세요. 아이템을 먹으면 특수 효과가 발동합니다!")

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

<canvas id="myCanvas" width="480" height="360"></canvas>

<script>
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");

    // 스테이지 데이터 (1~3단계)
    const stages = [
        { rows: 3, cols: 5, speed: 2.5, name: "Stage 1" },
        { rows: 4, cols: 6, speed: 3.5, name: "Stage 2" },
        { rows: 5, cols: 6, speed: 4.5, name: "Stage 3 (FINAL)" }
    ];

    let currentStage = 0;
    
    // 게임 상태 변수
    let x, y, dx, dy;
    const ballRadius = 7;
    
    let paddleHeight = 10;
    let paddleWidth = 80;
    let paddleX;
    
    let rightPressed = false;
    let leftPressed = false;

    let score = 0;
    let bricks = [];
    let items = [];
    let gameOver = false;
    let gameWon = false;

    // 아이템 종류
    const itemTypes = [
        { type: 'expand', color: '#00FF00', label: 'P' },  // 패들 확대
        { type: 'shrink', color: '#FF0000', label: 'S' },  // 패들 축소
        { type: 'bonus', color: '#FFFF00', label: 'B' }    // 보너스 점수
    ];

    function initStage(stageIdx) {
        const config = stages[stageIdx];
        x = canvas.width / 2;
        y = canvas.height - 30;
        
        // 공 방향 설정 (속도 반영)
        dx = config.speed * (Math.random() > 0.5 ? 1 : -1);
        dy = -config.speed;
        
        paddleX = (canvas.width - paddleWidth) / 2;

        const brickWidth = (canvas.width - 60 - (config.cols - 1) * 8) / config.cols;
        const brickHeight = 16;
        const brickPadding = 8;
        const brickOffsetTop = 40;
        const brickOffsetLeft = 30;

        bricks = [];
        for (let c = 0; c < config.cols; c++) {
            bricks[c] = [];
            for (let r = 0; r < config.rows; r++) {
                bricks[c][r] = { 
                    x: 0, 
                    y: 0, 
                    w: brickWidth, 
                    h: brickHeight, 
                    padding: brickPadding,
                    offsetTop: brickOffsetTop,
                    offsetLeft: brickOffsetLeft,
                    status: 1 
                };
            }
        }
        items = [];
    }

    document.addEventListener("keydown", (e) => {
        if (e.key === "Right" || e.key === "ArrowRight") rightPressed = true;
        else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = true;
    });

    document.addEventListener("keyup", (e) => {
        if (e.key === "Right" || e.key === "ArrowRight") rightPressed = false;
        else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = false;
    });

    document.addEventListener("mousemove", (e) => {
        const relativeX = e.clientX - canvas.offsetLeft;
        if (relativeX > 0 && relativeX < canvas.width) {
            paddleX = relativeX - paddleWidth / 2;
        }
    });

    function spawnItem(x, y) {
        if (Math.random() < 0.35) { // 35% 확률로 아이템 드롭
            const randomItem = itemTypes[Math.floor(Math.random() * itemTypes.length)];
            items.push({
                x: x,
                y: y,
                dy: 2,
                radius: 10,
                ...randomItem
            });
        }
    }

    function updateItems() {
        for (let i = items.length - 1; i >= 0; i--) {
            let item = items[i];
            item.y += item.dy;

            // 패들 아이템 획득 검사
            if (
                item.y + item.radius >= canvas.height - paddleHeight - 5 &&
                item.x >= paddleX && 
                item.x <= paddleX + paddleWidth
            ) {
                if (item.type === 'expand') {
                    paddleWidth = Math.min(paddleWidth + 25, 140);
                } else if (item.type === 'shrink') {
                    paddleWidth = Math.max(paddleWidth - 20, 40);
                } else if (item.type === 'bonus') {
                    score += 50;
                }
                items.splice(i, 1);
                continue;
            }

            // 바닥에 떨어지면 제거
            if (item.y > canvas.height) {
                items.splice(i, 1);
            }
        }
    }

    function collisionDetection() {
        const config = stages[currentStage];
        let activeBricks = 0;

        for (let c = 0; c < config.cols; c++) {
            for (let r = 0; r < config.rows; r++) {
                const b = bricks[c][r];
                if (b.status === 1) {
                    activeBricks++;
                    if (x > b.x && x < b.x + b.w && y > b.y && y < b.y + b.h) {
                        dy = -dy;
                        b.status = 0;
                        score += 10;
                        spawnItem(b.x + b.w / 2, b.y + b.h);

                        // 모든 벽돌을 깨트린 경우
                        if (activeBricks - 1 === 0) {
                            if (currentStage + 1 < stages.length) {
                                currentStage++;
                                initStage(currentStage);
                            } else {
                                gameWon = true;
                            }
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
        const colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"];
        const config = stages[currentStage];
        for (let c = 0; c < config.cols; c++) {
            for (let r = 0; r < config.rows; r++) {
                if (bricks[c][r].status === 1) {
                    const b = bricks[c][r];
                    const brickX = c * (b.w + b.padding) + b.offsetLeft;
                    const brickY = r * (b.h + b.padding) + b.offsetTop;
                    b.x = brickX;
                    b.y = brickY;
                    ctx.beginPath();
                    ctx.rect(brickX, brickY, b.w, b.h);
                    ctx.fillStyle = colors[r % colors.length];
                    ctx.fill();
                    ctx.closePath();
                }
            }
        }
    }

    function drawItems() {
        items.forEach(item => {
            ctx.beginPath();
            ctx.arc(item.x, item.y, item.radius, 0, Math.PI * 2);
            ctx.fillStyle = item.color;
            ctx.fill();
            ctx.closePath();

            ctx.font = "bold 11px sans-serif";
            ctx.fillStyle = "#000000";
            ctx.textAlign = "center";
            ctx.fillText(item.label, item.x, item.y + 4);
        });
    }

    function drawUI() {
        ctx.font = "14px sans-serif";
        ctx.fillStyle = "#FFFFFF";
        ctx.textAlign = "left";
        ctx.fillText("Score: " + score, 10, 22);
        ctx.textAlign = "right";
        ctx.fillText(stages[currentStage].name, canvas.width - 10, 22);
    }

    function drawMessage(text, color) {
        ctx.font = "bold 26px sans-serif";
        ctx.fillStyle = color;
        ctx.textAlign = "center";
        ctx.fillText(text, canvas.width / 2, canvas.height / 2);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        drawBricks();
        drawBall();
        drawPaddle();
        drawItems();
        drawUI();
        
        collisionDetection();
        updateItems();

        if (gameWon) {
            drawMessage("ALL STAGES CLEARED! 🎉", "#00CC96");
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
                let hitPoint = (x - (paddleX + paddleWidth / 2)) / (paddleWidth / 2);
                dx = hitPoint * stages[currentStage].speed * 1.2;
                dy = -Math.abs(dy);
            } else if (y + dy > canvas.height) {
                gameOver = true;
            }
        }

        // 키보드 조작
        if (rightPressed && paddleX < canvas.width - paddleWidth) {
            paddleX += 6;
        } else if (leftPressed && paddleX > 0) {
            paddleX -= 6;
        }

        x += dx;
        y += dy;

        requestAnimationFrame(draw);
    }

    initStage(0);
    draw();
</script>
</body>
</html>
"""

components.html(game_html, height=390)

st.markdown("---")
st.markdown("""
**🎮 아이템 안내**
* 🟢 **P**: 패들 길이 증가
* 🔴 **S**: 패들 길이 감소
* 🟡 **B**: 보너스 점수 (+50점)
""")
