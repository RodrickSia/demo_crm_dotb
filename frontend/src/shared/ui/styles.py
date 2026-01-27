ACTION_CARD_CSS = """
<style>
.action-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}
.action-card:hover {
    transform: translateY(-5px);
}
.score-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: conic-gradient(#4ade80 0deg, #22c55e 180deg, #16a34a 360deg);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px auto;
    position: relative;
}
.score-inner {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    font-weight: bold;
    color: #16a34a;
}
.action-title {
    font-size: 18px;
    font-weight: bold;
    margin-top: 10px;
}
</style>
"""
