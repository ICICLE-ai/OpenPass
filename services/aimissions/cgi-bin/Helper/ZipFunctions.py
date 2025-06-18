import shutil

def zipFile(src_path, dst_path):
    shutil.make_archive(dst_path, 'zip', src_path)


def unzipFile(src_path, dst_path):
    shutil.unpack_archive(src_path, dst_path, 'zip')
