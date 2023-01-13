from file_system import FileSystem
import pytest

@pytest.fixture
def file_system():
    fs = FileSystem(5, 5)
    fs.mkdir("/directory")
    return fs

@pytest.fixture
def file_system_dir_overflow():
    fs = FileSystem(5, 5)
    fs.mkdir("/directory1")
    fs.create_binary_file("/directory1", "one1.bin")
    fs.create_binary_file("/directory1", "two2.bin")
    fs.create_binary_file("/directory1", "three3.bin")
    fs.create_binary_file("/directory1", "four4.bin")
    fs.create_binary_file("/directory1", "five5.bin")
    return fs

@pytest.fixture
def file_system_with_files():
    fs = FileSystem(5, 5)
    fs.mkdir("/directory1")
    fs.mkdir("/directory1/directory1-1")
    fs.mkdir("/directory1/directory1-2")

    fs.create_binary_file("/directory1/directory1-1", "bin.bin")
    fs.create_log_file("/directory1/directory1-1", "log.log")
    fs.create_buf_file("/directory1/directory1-2", "buf.buf")
    fs.create_log_file("/directory1/directory1-2", "log.log")
    return fs

#-------------------------------------------------------------------

def test_create_binary_file_simple_good(file_system):
    file_system.create_binary_file("/directory", "bin.bin")
    assert file_system.ls("/directory") == ['bin.bin']

def test_create_binary_file_dirs_missing_good(file_system):
    file_system.create_binary_file("/directory/directory1/directory2", "bin.bin")
    assert file_system.ls("/directory/directory1/directory2") == ['bin.bin']

def test_create_binary_file_no_directory_bad():
    fs = FileSystem(5, 5)
    assert fs.create_binary_file("/", "bin.bin") == False

def test_create_binary_file_incorrect_extencion_bad(file_system):
    assert file_system.create_binary_file("/directory", "anth.bi") == False


def test_create_binary_file_already_exists_bad(file_system_with_files):
    assert file_system_with_files.create_binary_file("/directory1/directory1-1", "bin.bin") == False

def test_create_binary_file_impossible_path(file_system):
    assert file_system.create_binary_file("/directory/directory.bin", "anth.bin") == False

def test_create_binary_file_dir_is_full_bad(file_system_dir_overflow):
    assert file_system_dir_overflow.create_binary_file("/directory1", "anth.bin") == False


# -----------------------------------------------------------------------------------------------

def test_move_binary_file_simple_good_1(file_system_with_files):
    file_system_with_files.move_binary_file("/directory1/directory1-1/bin.bin", "/directory1/directory1-2")
    assert file_system_with_files.ls("/directory1/directory1-1") == ['log.log']


def test_move_binary_file_simple_good_2(file_system_with_files):
    file_system_with_files.move_binary_file("/directory1/directory1-1/bin.bin", "/directory1/directory1-2")
    assert file_system_with_files.ls("/directory1/directory1-2") == ['bin.bin', 'buf.buf', 'log.log']


def test_move_binary_file_overflow(file_system_dir_overflow):
    file_system_dir_overflow.create_binary_file("/directory2", "bin.bin")
    assert file_system_dir_overflow.move_binary_file("/directory2/bin.bin", "/directory1") == False


def test_move_binary_file_such_name_already_exists(file_system_with_files):
    file_system_with_files.create_binary_file("/directory1/directory1-2", "bin.bin")
    assert file_system_with_files.move_binary_file("/directory1/directory1-1/bin.bin",
                                                   "/directory1/directory1-2") == False

def test_move_binary_file_doesnt_exist(file_system_with_files):
    assert file_system_with_files.move_binary_file("/directory1/directory1-2/bin.bin",
                                                   "/directory1/directory1-1") == False

#-----------------------------------------------------------------------------------------------

def test_delete_binary_file_simple_good(file_system_with_files):
    file_system_with_files.delete_binary_file("/directory1/directory1-1/bin.bin")
    assert file_system_with_files.ls("/directory1/directory1-1") == ['log.log']

def test_delete_binary_file_doesnt_exist(file_system):
    assert file_system.delete_binary_file("/directory/bin.bin") == False

#-----------------------------------------------------------------------------------------------

def test_read_binary_file_simple_good(file_system_with_files):
    assert file_system_with_files.read_binary_file("/directory1/directory1-1/bin.bin") == "Just a bin file."

def test_read_binary_file_doesnt_exist_bad(file_system):
    assert file_system.read_binary_file("/directory/bin.bin") == None


