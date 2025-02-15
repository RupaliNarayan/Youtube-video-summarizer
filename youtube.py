
import whisper
import yt_dlp

import genai


def load_whisper_model():
    # Correct way to load the model (check your Whisper version)
    try:
        model = whisper.load_model("base")  # Try the standard way first
    except AttributeError:  # For older versions
        model = whisper.load_model("tiny")  # Try this if 'base' doesn't exist.
    return model


def generate_summary(st, video_link):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',  # Get best audio and video if no audio
            'noplaylist': True,  # Only download single videos, not playlists
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=False)  # Extract info first

            # Check if there are formats available. If not, raise exception.
            if 'formats' not in info_dict or not info_dict['formats']:
                raise ValueError("No suitable video or audio streams found.")

            # Find the best audio format or the best video format (if no audio)
            best_format = None
            for f in info_dict['formats']:
                if f.get('acodec') != 'none':  # Prioritize audio formats
                    best_format = f
                    break
            if best_format is None:
                for f in info_dict['formats']:
                    if f.get('vcodec') != 'none':  # If no audio, get video
                        best_format = f
                        break
            if best_format is None:
                raise ValueError("No suitable video or audio streams found.")

            video_path = ydl.prepare_filename(info_dict)  # Get the filename
            ydl_opts['outtmpl'] = video_path  # Set the output template
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])  # Download the file

            model = load_whisper_model()
            result = model.transcribe(video_path)
            transcript = result["text"]
            print(transcript)
            summary = genai.generate_summary_with_openai(st, transcript)

            return summary

    except yt_dlp.DownloadError as e:
        st.error(f"Download error: {e}")
        return None
    except ValueError as e:
        st.error(f"Error: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None
