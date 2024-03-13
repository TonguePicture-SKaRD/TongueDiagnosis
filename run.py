import threading
import uvicorn
from application import create_app
from application.net.predict import TonguePredictor

app = create_app()
if __name__ == '__main__':
    tonguePredictor = TonguePredictor()
    threading.Thread(target=tonguePredictor.main).start()
    uvicorn.run(app, host="127.0.0.1", port=5000)
