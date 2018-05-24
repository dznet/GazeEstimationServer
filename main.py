from app import gaze_estimation

app = gaze_estimation('development')

if __name__ == '__main__':
    app.run(app.config.HOST,
            app.config.PORT)
