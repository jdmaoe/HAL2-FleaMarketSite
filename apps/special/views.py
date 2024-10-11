from flask import Blueprint, request, render_template, current_app, send_file
import os
import subprocess
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
import wave
from pydub import AudioSegment
import pysrt


# Blueprintでgameアプリを生成する
special = Blueprint(
  'special',
  __name__,
  template_folder='templates',
  static_folder='static'
  )


# Google Cloud認証情報の設定
credentials = service_account.Credentials.from_service_account_file('secret.json')
client = speech.SpeechClient(credentials=credentials)


# WAVファイルのサンプルレートを取得
def get_wav_sample_rate(wav_filename):
    with wave.open(wav_filename, 'rb') as wf:
        return wf.getframerate()


# wavファイルを5秒ごとに分割
def split_wav_file(wav_filename):
    # pydubでwavファイルを読み込む
    sound = AudioSegment.from_wav(wav_filename)
    # 3秒ごとに分割
    split_wav_files = []
    for i in range(0, len(sound), 5000):
        split_wav_files.append(sound[i:i+5000])

    return split_wav_files


# 分割されたwavファイルをGoogle Cloud Speech APIに送信
def recognize_wav_files(wav_files, config):
    subtitles = []
    for wav_file in wav_files:
        # wavファイルをバイナリデータに変換
        content = wav_file.raw_data
        audio = speech.RecognitionAudio(content=content)

        # Google Cloud Speech APIに送信
        response = client.recognize(config=config, audio=audio)

        # 認識結果をリストに追加
        for result in response.results:
            subtitles.append(result.alternatives[0].transcript)

    return subtitles


# 字幕データをSRTフォーマットで保存
def save_subtitles_srt(subtitles, mp4_filename):
    # 字幕データをSRTフォーマットで保存
    srt_filename = os.path.splitext(mp4_filename)[0] + '.srt'
    subs = pysrt.SubRipFile()
    for i, subtitle in enumerate(subtitles):
        subs.append(pysrt.SubRipItem(
            index=i,
            start=pysrt.SubRipTime(0, 0, i * 5),
            end=pysrt.SubRipTime(0, 0, (i + 1) * 5),
            text=subtitle
        ))
    # 保存
    subs.save(srt_filename, encoding='utf-8')
    # 保存したファイル名を返す
    return srt_filename


# srtファイルをassファイルに変換
def srt_to_ass(srt_filename, ass_filename):
    try:
        # FFmpegコマンドを構築
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', srt_filename,
            ass_filename
        ]

        # FFmpegコマンドを実行
        subprocess.run(ffmpeg_cmd, check=True)
        print(f'{srt_filename} を {ass_filename} に変換しました。')
    except subprocess.CalledProcessError as e:
        print(f'変換中にエラーが発生しました: {e}')


def delete_file_if_exists(filename):
    file_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{filename} を削除しました")
    else:
        print(f"{filename} は存在しません")


def add_newline_halfway(subtitles):
    new_subtitles = []
    for subtitle in subtitles:
        halfway_index = len(subtitle) // 2
        new_subtitle = subtitle[:halfway_index] + r"\N" + subtitle[halfway_index:]
        new_subtitles.append(new_subtitle)
    return new_subtitles


# gameページを作成する
@special.route('/game')
def game():
    return render_template('special/game.html')


# dropページを作成する
@special.route('/drop')
def drop():
    return render_template('special/drop.html')


# quizページを作成する
@special.route('/quiz')
def quiz():
    return render_template('special/quiz.html')


# indexのルーティング
@special.route('/video_conversion', methods=['GET', 'POST'])
def video_conversion():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "ファイルが選択されていません"

        file = request.files['file']

        if file.filename == '':
            return "ファイルが選択されていません"

        if file:
            delete_file_if_exists('output.mp4')
            mp4_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], 'input.mp4')
            file.save(mp4_filename)

            # MP4ファイルをWAVに変換
            wav_filename = os.path.splitext(mp4_filename)[0] + '.wav'
            subprocess.call(['ffmpeg', '-i', mp4_filename, wav_filename])

            # WAVファイルのサンプルレートを取得
            wav_sample_rate = get_wav_sample_rate(wav_filename)

            # WAVファイルのサンプルレートをAPIの設定に適用
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=wav_sample_rate,
                language_code="ja-JP",
            )

            # WAVファイルを5秒ごとに分割
            split_wav_files = split_wav_file(wav_filename)

            # 分割されたwavファイルをGoogle Cloud Speech APIに送信
            subtitles = recognize_wav_files(split_wav_files, config)

            # 途中で改行を入れる
            subtitles = add_newline_halfway(subtitles)

            # 字幕データをSRTフォーマットで保存
            srt_filename = save_subtitles_srt(subtitles, mp4_filename)

            # srtファイルをassファイルに変換
            ass_filename = os.path.splitext(srt_filename)[0] + '.ass'

            ass_filename = r'C:/HAL2/IA22/HEW/apps/images/sam.ass'

            srt_to_ass(srt_filename, ass_filename)

            ass_filename = r'apps/images/sam.ass'

            output_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], 'output.mp4')
            ffmpeg_cmd = ['ffmpeg', '-i', mp4_filename, '-vf', f'ass={ass_filename}', output_filename,]
            subprocess.run(ffmpeg_cmd, check=True)

            # sam.assファイルを削除
            delete_file_if_exists('sam.ass')
            delete_file_if_exists('input.mp4')
            delete_file_if_exists('input.wav')
            delete_file_if_exists('input.srt')

            return send_file(output_filename, as_attachment=True)
        else:
            return render_template('out.html')
    else:
        return render_template('special/video_conversion.html')
