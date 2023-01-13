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


#-------------------------------------------------------------------------------------
def test_ls_1(file_system_with_files):
    assert file_system_with_files.ls("/directory1/directory1-1") == ['bin.bin', 'log.log']

def test_ls_2(file_system_with_files):
    assert file_system_with_files.ls("/directory1/directory1-2") == ['buf.buf', 'log.log']

def test_ls_3(file_system_with_files):
    assert file_system_with_files.ls("/") == ['directory1']
    
#-------------------------------------------------------------------------------------

def test_mkdir_simple_good(file_system):
    file_system.mkdir("/directory")
    assert file_system.ls("/") == ['directory']

def test_mkdir_nested_good(file_system_with_files):
    file_system_with_files.mkdir("/directory1/directory1-3")
    assert file_system_with_files.ls("/directory1") == ['directory1-1', 'directory1-2', 'directory1-3']

def test_mkdir_overflow_bad(file_system_dir_overflow):
    assert file_system_dir_overflow.mkdir("/directory1/directory2") == False

def test_mkdir_incorrect_path_bad(file_system):
    assert file_system.mkdir("/baddirectory.log") == False

def test_mkdir_some_dirs_missing(file_system):
    file_system.mkdir("/directory1/directory2")
    assert file_system.ls("/directory1") == ['directory2']
#---------------------------------------------------------------------------------------
