from flask import Flask, request, jsonify
import instaloader

app = Flask(__name__)
L = instaloader.Instaloader()

@app.route('/download', methods=['GET'])
def download_instagram():
    url = request.args.get('url')  # Ambil parameter URL dari query

    if not url:
        return jsonify({"error": "Parameter 'url' diperlukan"}), 400

    try:
        shortcode = url.split("/")[-2]  # Ambil shortcode dari URL
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        data = {
            "username": post.owner_username,
            "caption": post.caption,
            "media_url": post.video_url if post.is_video else post.url,
            "is_video": post.is_video
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
