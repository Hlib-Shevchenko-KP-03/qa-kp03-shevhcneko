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


#--------------------------------------------------------------

def test_create_buf_file_simple_good(file_system):
    file_system.create_buf_file("/directory", "buf.buf")
    assert file_system.ls("/directory") == ['buf.buf']

def test_create_buf_file_dirs_missing_good(file_system):
    file_system.create_buf_file("/directory/directory1/directory2", "buf.buf")
    assert file_system.ls("/directory/directory1/directory2") == ['buf.buf']

def test_create_buf_file_no_directory_bad():
    fs = FileSystem(5, 5)
    assert fs.create_buf_file("/", "buf.buf") == False

def test_create_buf_file_already_exists_bad(file_system_with_files):
    assert file_system_with_files.create_buf_file("/directory1/directory1-2", "buf.buf") == False

def test_create_buf_file_impossible_path(file_system):
    assert file_system.create_buf_file("/directory/directory.buf", "smth.buf") == False

def test_create_buf_file_incorrect_extencion_bad(file_system):
    assert file_system.create_buf_file("/directory", "smth.bu") == False

def test_create_buf_file_dir_is_full_bad(file_system_dir_overflow):
    assert file_system_dir_overflow.create_buf_file("/directory1", "smth.buf") == False

#--------------------------------------------------------------------------------------------

def test_delete_buf_file_simple_good(file_system_with_files):
    file_system_with_files.delete_buf_file("/directory1/directory1-2/buf.buf")
    assert file_system_with_files.ls("/directory1/directory1-2") == ['log.log']

def test_delete_buf_file_doesnt_exist(file_system):
    assert file_system.delete_buf_file("/directory/buf.buf") == False

#--------------------------------------------------------------------------------------------

def test_buf_file_simple_good(file_system_with_files):
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "some element")
    assert file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf") == "some element"

def test_buf_file_several_elems(file_system_with_files):
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "first elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "second elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "third elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "fourth elem")
    assert file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "fifth elem") == True

def test_consume_several_elems(file_system_with_files):
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "first elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "second elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "third elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "fourth elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "fifth elem")

    file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf")
    file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf")
    file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf")
    file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf")
    assert file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf") == "fifth elem"

def test_buf_file_consume_empty_file(file_system_with_files):
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "first elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "second elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "third elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "fourth elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "fifth elem")

    file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf")
    file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf")
    file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf")
    file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf")
    file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf")
    assert file_system_with_files.consume_from_buf_file("/directory1/directory1-2/buf.buf") == False
    
def test_buf_file_overflow(file_system_with_files):
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "first elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "second elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "third elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "fourth elem")
    file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "fifth elem")
    assert file_system_with_files.push_to_buf_file("/directory1/directory1-2/buf.buf", "error elem") == False

    
    
    
    