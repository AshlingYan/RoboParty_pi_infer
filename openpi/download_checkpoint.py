from openpi.shared import download

# 下载 pi05_libero  checkpoint
checkpoint_path = download.maybe_download(
    "gs://openpi-assets/checkpoints/pi05_libero",
    gs={"token": "anon"}  # 匿名访问
)
print(f"Checkpoint 下载完成，路径：{checkpoint_path}")