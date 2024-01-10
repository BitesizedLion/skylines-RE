import struct
import os
from pprint import pprint # remove if you dont want pretty print


def read_pstr(file):
    length = struct.unpack("B", file.read(1))[0]
    return file.read(length).decode("utf-8")


def read_uint16(file):
    return struct.unpack("<H", file.read(2))[0]


def read_uint32(file):
    return struct.unpack("<I", file.read(4))[0]


def read_uint64(file):
    return struct.unpack("<Q", file.read(8))[0]


def read_asset_entry(file):
    name = read_pstr(file)
    checksum = read_pstr(file)
    asset_type = read_uint32(file)
    offset = read_uint64(file)
    size = read_uint64(file)
    return {
        "Name": name,
        "Checksum": checksum,
        "Type": asset_type,
        "Offset": offset,
        "Size": size,
    }


def read_crp_header(file):
    signature = file.read(4).decode("utf-8")
    version = read_uint16(file)
    package_name = read_pstr(file)
    author_name = read_pstr(file)
    package_version = read_uint32(file)
    main_asset_name = read_pstr(file)
    file_count = read_uint32(file)
    data_offset = read_uint64(file)
    asset_entries = [read_asset_entry(file) for _ in range(file_count)]

    return {
        "Signature": signature,
        "Version": version,
        "Package Name": package_name,
        "Author Name": author_name,
        "Package Version": package_version,
        "Main Asset Name": main_asset_name,
        "File Count": file_count,
        "Data Offset": data_offset,
        "Asset Entries": asset_entries,
    }


def dump_assets(file, output_directory):
    crp_header = read_crp_header(file)
    pprint(crp_header) # remove if you dont want pretty print

    for entry in crp_header["Asset Entries"]:
        file.seek(crp_header["Data Offset"] + entry["Offset"])
        asset_data = file.read(entry["Size"])

        # Create a directory for each asset type
        asset_type_directory = os.path.join(output_directory, str(entry["Type"]))
        os.makedirs(asset_type_directory, exist_ok=True)

        # Write asset data to a file
        asset_filename = os.path.join(asset_type_directory, entry["Name"])
        with open(asset_filename, "wb") as asset_file:
            asset_file.write(asset_data)


crp_filename = "Regal.crp" # change name
output_directory = "regal_output_assets" # change directory

with open(crp_filename, "rb") as file:
    dump_assets(file, output_directory)
