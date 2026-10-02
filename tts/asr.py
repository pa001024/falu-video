"""用 GPT-SoVITS 自带的 FunASR（paraformer-large 中文）转写音频。

用法：runtime/python.exe asr.py <out.json> <wav1> [<wav2> ...]
输出：{wav 路径: 转写文本}
"""
import json
import os
import sys

GSV_ROOT = r"E:\soft\GPT-SoVITS-v2"
os.chdir(GSV_ROOT)
sys.path.insert(0, GSV_ROOT)

from funasr import AutoModel  # noqa: E402

ASR_DIR = os.path.join(GSV_ROOT, "tools", "asr", "models")


def create_model(with_punc: bool) -> AutoModel:
    """
    加载本地 paraformer 模型（不联网）。
    @param with_punc 是否附带标点模型；校验发音时不需要标点
    @returns FunASR AutoModel 实例
    """
    kwargs = dict(
        model=os.path.join(ASR_DIR, "speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"),
        model_revision="v2.0.4",
        vad_model=os.path.join(ASR_DIR, "speech_fsmn_vad_zh-cn-16k-common-pytorch"),
        vad_model_revision="v2.0.4",
        disable_update=True,
    )
    if with_punc:
        kwargs.update(
            punc_model=os.path.join(ASR_DIR, "punc_ct-transformer_zh-cn-common-vocab272727-pytorch"),
            punc_model_revision="v2.0.4",
        )
    return AutoModel(**kwargs)


def main() -> None:
    out_path = sys.argv[1]
    wavs = sys.argv[2:]
    model = create_model(with_punc=False)
    result = {}
    for wav in wavs:
        try:
            res = model.generate(input=wav)
            result[wav] = "".join(r.get("text", "") for r in res).replace(" ", "")
        except Exception as err:  # 单条失败不影响其余
            result[wav] = f"<ERROR {err}>"
    with open(out_path, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
