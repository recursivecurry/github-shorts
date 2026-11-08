from functools import lru_cache
import json
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT, FPS = 1080, 1920, 30
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
BG, PANEL, LINE = "#101217", "#1D2330", "#3B4354"
WHITE, MUTED, MINT, PURPLE = "#F4F6FA", "#B4BDCE", "#78E3D0", "#B4A2FF"
SCENES = [
    {
        "start": 0, "end": 5,
        "title": ["코드 변경을", "짧은 영상으로"],
        "narration": "깃허브 쇼츠는 코드 변경 내용을 짧은 영상으로 설명해 줘요.",
        "captions": ["깃허브 쇼츠는 코드 변경 내용을", "짧은 영상으로 설명해 줘요."],
    },
    {
        "start": 5, "end": 11,
        "title": ["어려운 변경도", "그림으로 쉽게"],
        "narration": "리뷰할 코드와 관련 이슈를 읽고, 쉬운 그림과 설명을 만들어요.",
        "captions": ["리뷰할 코드와 관련 이슈를 읽고,", "쉬운 그림과 설명을 만들어요."],
    },
    {
        "start": 11, "end": 17,
        "title": ["쇼츠처럼 넘기며", "보고 이해해요"],
        "narration": "휴대폰이나 컴퓨터에서 영상을 봐요. 위아래로 넘기면 다음 코드가 나와요.",
        "captions": ["휴대폰이나 컴퓨터에서 영상을 봐요.", "위아래로 넘기면 다음 코드가 나와요."],
    },
    {
        "start": 17, "end": 23,
        "title": ["퀴즈를 맞히면", "리뷰할 수 있어요"],
        "narration": "영상 끝의 퀴즈를 맞히면, 승인을 하거나 변경을 요구할 수 있어요.",
        "captions": ["영상 끝의 퀴즈를 맞히면,", "승인을 하거나 변경을 요구할 수 있어요."],
    },
    {
        "start": 23, "end": 30,
        "title": ["리뷰 버튼은", "언제 켜질까요?"],
        "narration": "확인 퀴즈! 리뷰 버튼은 언제 켜질까요? 네 가지 중에서 골라 보세요.",
        "captions": ["확인 퀴즈! 리뷰 버튼은 언제 켜질까요?", "네 가지 중에서 골라 보세요."],
    },
]
CHOICES = ["영상을 켜면", "댓글을 남기면", "퀴즈의 정답을 맞히면", "링크를 공유하면"]


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=True, capture_output=True, text=True)


@lru_cache(maxsize=64)
def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=6 if bold else 0)


def text(draw: ImageDraw.ImageDraw, xy: tuple, value: str, size: int = 44,
         fill: str = WHITE, bold: bool = False, anchor: str = "mm") -> None:
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def box(draw: ImageDraw.ImageDraw, bounds: tuple, fill: str = PANEL,
        outline: str | None = None, radius: int = 32) -> None:
    draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=3)


def arrow(draw: ImageDraw.ImageDraw, x: int, y: int, color: str = MINT) -> None:
    draw.line([(x, y), (x, y + 54)], fill=color, width=7)
    draw.line([(x - 17, y + 36), (x, y + 54), (x + 17, y + 36)], fill=color, width=7)


def play(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1) -> None:
    r = int(69 * scale)
    draw.ellipse((x - r, y - r, x + r, y + r), fill=MINT)
    draw.polygon([(x - r * .22, y - r * .43), (x - r * .22, y + r * .43),
                  (x + r * .48, y)], fill=BG)


def scene_image(index: int) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    for y in range(HEIGHT):
        amount = max(0, 1 - abs(y - 870) / 850)
        draw.line((0, y, WIDTH, y), fill=(16 + int(4 * amount), 18 + int(12 * amount),
                                       23 + int(20 * amount)))
    draw.line([(78, 80), (78, 130), (105, 130), (105, 102)], fill=MINT, width=6)
    for x, y in [(78, 80), (78, 130), (105, 102)]:
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=MINT)
    text(draw, (135, 105), "github-shorts", 39, bold=True, anchor="lm")
    box(draw, (810, 73, 1008, 138), outline=LINE, radius=30)
    text(draw, (909, 104), "30초 소개", 29, MUTED)
    text(draw, (72, 230), "이해 확인" if index == 4 else f"0{index + 1} / 서비스 소개",
         31, MINT, anchor="lm")
    for line_index, line in enumerate(SCENES[index]["title"]):
        text(draw, (72, 330 + line_index * 103), line, 78,
             MINT if line_index else WHITE, True, "lm")

    if index == 0:
        box(draw, (160, 590, 920, 825), outline=LINE)
        text(draw, (245, 648), "PR", 37, PURPLE, True)
        text(draw, (575, 648), "고친 코드를 보여 주세요", 38)
        for y, length, color in [(710, 440, MUTED), (750, 540, MINT)]:
            draw.rounded_rectangle((230, y, 230 + length, y + 12), radius=6, fill=color)
        arrow(draw, 540, 862)
        box(draw, (287, 960, 793, 1345), "#263B45", outline=MINT, radius=44)
        play(draw, 540, 1095, 1.1)
        text(draw, (540, 1230), "음성 + 그림 + 자막", 40, WHITE, True)
        text(draw, (540, 1395), "리뷰 전에, 먼저 이해해요", 35, MUTED)
    elif index == 1:
        for row, (label, detail, symbol, color) in enumerate([
            ("코드와 이슈", "무엇이 바뀌었을까?", "PR", PURPLE),
            ("쉬운 설명", "그림으로 흐름을 한눈에", "eli5", MINT),
            ("설명 영상", "한국어 음성과 자막까지", "30s", PURPLE),
        ]):
            y = 600 + row * 275
            box(draw, (110, y, 970, y + 204), outline=LINE)
            box(draw, (147, y + 37, 290, y + 169), "#2E3447", radius=27)
            text(draw, (219, y + 103), symbol, 40, color, True)
            text(draw, (333, y + 70), label, 45, WHITE, True, "lm")
            text(draw, (333, y + 140), detail, 34, MUTED, anchor="lm")
            if row < 2:
                arrow(draw, 540, y + 214)
    elif index == 2:
        box(draw, (225, 554, 810, 1376), "#080B11", outline=LINE, radius=56)
        box(draw, (250, 582, 785, 1348), "#244649", radius=40)
        text(draw, (301, 632), "▶  소리", 28, WHITE, anchor="lm")
        text(draw, (725, 632), "필터", 28, WHITE)
        text(draw, (505, 799), "무엇이", 62, WHITE, True)
        text(draw, (505, 875), "바뀌었을까?", 62, MINT, True)
        box(draw, (292, 956, 669, 1088), "#142A32", radius=24)
        text(draw, (480, 1022), "변경 전  →  변경 후", 33)
        for y, label in [(999, "반응"), (1097, "댓글"), (1195, "리뷰")]:
            draw.ellipse((696, y - 31, 758, y + 31), fill="#172E37")
            text(draw, (727, y), label, 22)
        text(draw, (285, 1202), "@작성자  ·  조금 전", 27, anchor="lm")
        text(draw, (285, 1258), "org / repo   #개선", 28, anchor="lm")
        for y in [688, 783]:
            draw.line([(888, y + 20), (918, y - 10), (948, y + 20)], fill=MINT, width=8)
        text(draw, (540, 1440), "PC와 모바일 웹에서", 34, MUTED)
    elif index == 3:
        box(draw, (135, 585, 945, 1040), outline=LINE)
        text(draw, (540, 655), "내용을 이해했나요?", 44, WHITE, True)
        for row in range(2):
            for col in range(2):
                choice = row * 2 + col
                x, y = 180 + col * 375, 730 + row * 135
                box(draw, (x, y, x + 345, y + 108), "#183C35" if choice == 2 else "#292F40",
                    MINT if choice == 2 else LINE, 23)
                text(draw, (x + 172, y + 54), f"{chr(65 + choice)}  " +
                     ("정답!" if choice == 2 else "보기"), 37, MINT if choice == 2 else MUTED,
                     choice == 2)
        arrow(draw, 540, 1090)
        text(draw, (540, 1200), "리뷰 버튼이 켜져요", 42, MINT, True)
        box(draw, (135, 1285, 512, 1405), MINT)
        box(draw, (545, 1285, 945, 1405), PURPLE)
        text(draw, (323, 1345), "승인", 45, BG, True)
        text(draw, (745, 1345), "변경 요구", 45, BG, True)
    else:
        for choice, label in enumerate(CHOICES):
            y = 645 + choice * 178
            box(draw, (75, y, 1005, y + 140), outline=LINE)
            box(draw, (101, y + 28, 185, y + 112), "#30364C", radius=20)
            text(draw, (143, y + 70), chr(65 + choice), 39, PURPLE, True)
            text(draw, (220, y + 70), label, 42, WHITE, anchor="lm")
        text(draw, (540, 1430), "정답과 해설은 설명 페이지에서 확인하세요", 30, MUTED)

    text(draw, (540, 1778), "PR  →  설명 영상  →  퀴즈  →  리뷰", 31, MUTED)
    draw.rounded_rectangle((72, 1830, 1008, 1838), radius=4, fill=LINE)
    return image


def prepare_audio() -> None:
    filters = []
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for index, scene in enumerate(SCENES):
        source = ROOT / f"voice-{index + 1}.txt"
        source.write_text(scene["narration"], encoding="utf-8")
        audio = ROOT / f"voice-{index + 1}.aiff"
        run(["say", "-v", "Yuna", "-r", "205", "-f", str(source), "-o", str(audio)])
        duration = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", str(audio)]).stdout)
        target = scene["end"] - scene["start"]
        speed = max(1, duration / (target - .4))
        if speed > 1.35:
            raise ValueError(f"Scene {index + 1} narration is too long: {duration:.2f}s")
        scene["source_audio_seconds"] = duration
        scene["audio_speed"] = speed
        scene["speech_end"] = scene["start"] + .15 + duration / speed
        command += ["-i", str(audio)]
        filters.append(f"[{index}:a]atempo={speed:.6f},adelay=150:all=1,"
                       f"apad,atrim=duration={target},asetpts=PTS-STARTPTS[a{index}]")
        print(f"Scene {index + 1}: {duration:.2f}s narration, {target}s slot, speed {speed:.3f}",
              flush=True)
    filters.append("".join(f"[a{i}]" for i in range(len(SCENES))) +
                   f"concat=n={len(SCENES)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11[out]")
    run(command + ["-filter_complex", ";".join(filters), "-map", "[out]", "-ar", "48000",
                   "-ac", "1", str(ROOT / "narration.wav")])


def render_video() -> None:
    backgrounds = [scene_image(i) for i in range(len(SCENES))]
    for index, image in enumerate(backgrounds):
        image.save(ROOT / f"scene-{index + 1}.png")
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
               "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
               "-i", str(ROOT / "narration.wav"), "-map", "0:v", "-map", "1:a",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "160k", "-t", "30", "-movflags", "+faststart",
               str(ROOT / "github-shorts-eli5-30s.mp4")]
    with (ROOT / "render.log").open("w") as log:
        with subprocess.Popen(command, stdin=subprocess.PIPE, stderr=log) as encoder:
            try:
                for frame in range(FPS * 30):
                    t = frame / FPS
                    index = next(i for i, scene in enumerate(SCENES) if t < scene["end"])
                    scene = SCENES[index]
                    image = backgrounds[index].copy()
                    elapsed = t - scene["start"]
                    if elapsed < .25:
                        image = Image.blend(Image.new("RGB", image.size, BG), image,
                                            min(1, elapsed / .25))
                    draw = ImageDraw.Draw(image)
                    box(draw, (60, 1515, 1020, 1705), "#080C13", radius=30)
                    split = (scene["start"] + .15 + scene["speech_end"]) / 2
                    caption = scene["captions"][int(t >= split)]
                    text(draw, (540, 1605), caption, 41, WHITE, True)
                    draw.rounded_rectangle((72, 1830, 72 + 936 * ((frame + 1) / 900), 1838),
                                           radius=4, fill=MINT)
                    if index == 4:
                        text(draw, (955, 230), f"{math.ceil(30 - t)}초", 31, PURPLE)
                    encoder.stdin.write(image.tobytes())
                encoder.stdin.close()
                if encoder.wait() != 0:
                    raise RuntimeError((ROOT / "render.log").read_text())
            except BaseException:
                if not encoder.stdin.closed:
                    encoder.stdin.close()
                encoder.terminate()
                raise


def timestamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    return f"00:{milliseconds // 60000:02}:{milliseconds // 1000 % 60:02}.{milliseconds % 1000:03}"


def save_contract() -> None:
    contract = {"duration_seconds": 30, "quiz_start_seconds": 23, "scenes": SCENES,
                "quiz": {"question": "리뷰 버튼은 언제 켜질까요?", "choices": CHOICES,
                         "correct_choice_id": "C",
                         "explanation": "현재 영상의 퀴즈에 정답을 맞히면 리뷰할 수 있습니다. "
                         "단, 본인 PR에는 리뷰 버튼이 없고 영상과 현재 코드가 다르면 "
                         "새 영상이 게시될 때까지 리뷰 제출이 차단됩니다."},
                "tts": "macOS say / Yuna / local",
                "eli5_skill": "https://github.com/anthropics/claude-plugins-community/blob/main/eli5/skills/eli5/SKILL.md",
                "pipeline_note": "Codex에서 직접 만든 샘플이며 Claude Code → Codex CLI 통합 실행을 검증한 결과는 아닙니다."}
    (ROOT / "storyboard.json").write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8")
    cues = ["WEBVTT\n"]
    for scene in SCENES:
        start = scene["start"] + .15
        middle = (start + scene["speech_end"]) / 2
        for a, b, caption in [(start, middle, scene["captions"][0]),
                              (middle, scene["end"], scene["captions"][1])]:
            cues.append(f"{timestamp(a)} --> {timestamp(b)}\n{caption}\n")
    (ROOT / "captions.ko.vtt").write_text("\n".join(cues), encoding="utf-8")


if __name__ == "__main__":
    prepare_audio()
    save_contract()
    render_video()
    print(ROOT / "github-shorts-eli5-30s.mp4", flush=True)
