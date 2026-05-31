import argparse
import base64
import ctypes
import os
from pathlib import Path
from ctypes import POINTER, byref, cast, c_char, windll
from ctypes import wintypes


DEFAULT_API_KEY_FILE = Path(".secrets/deepseek_api_key.bin")


class DataBlob(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", POINTER(c_char))]


def dpapi_encrypt(raw: bytes) -> bytes:
    in_buffer = ctypes.create_string_buffer(raw, len(raw))
    in_blob = DataBlob(len(raw), cast(in_buffer, POINTER(c_char)))
    out_blob = DataBlob()
    success = windll.crypt32.CryptProtectData(byref(in_blob), None, None, None, None, 0, byref(out_blob))
    if not success:
        raise RuntimeError("DPAPI 加密失败")
    encrypted = ctypes.string_at(out_blob.pbData, out_blob.cbData)
    windll.kernel32.LocalFree(out_blob.pbData)
    return encrypted


def encode_api_key(api_key: str) -> bytes:
    encrypted = dpapi_encrypt(api_key.encode("utf-8"))
    return b"dpapi:" + base64.urlsafe_b64encode(encrypted)


def read_api_key_input(from_arg: str) -> str:
    if from_arg.strip():
        return from_arg.strip()
    return os.environ.get("DEEPSEEK_API_KEY", "").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="将 DeepSeek API Key 写入本地密文文件")
    parser.add_argument("--api-key", default="", help="直接传入 API Key；不传时读取环境变量 DEEPSEEK_API_KEY")
    parser.add_argument("--out", default=str(DEFAULT_API_KEY_FILE), help="输出文件路径")
    args = parser.parse_args()

    api_key = read_api_key_input(args.api_key)
    if not api_key:
        raise ValueError("未提供 API Key，请使用 --api-key 或设置 DEEPSEEK_API_KEY")

    output_file = Path(args.out)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(encode_api_key(api_key))
    print(f"已写入密文 API Key 文件: {output_file}")


if __name__ == "__main__":
    main()
