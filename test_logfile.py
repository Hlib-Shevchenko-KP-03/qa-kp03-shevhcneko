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
    fs.mkdir("/directory1/directory1-three3")

    fs.create_binary_file("/directory1/directory1-1", "bin.bin")
    fs.create_log_file("/directory1/directory1-1", "log.log")
    fs.create_buf_file("/directory1/directory1-2", "buf.buf")
    fs.create_log_file("/directory1/directory1-2", "log.log")
    return fs

#------------------------------td---------------------------------------------------------------

def test_delete_log_file_simple_good(file_system_with_files):
    file_system_with_files.delete_log_file("/directory1/directory1-1/log.log")
    assert file_system_with_files.ls("/directory1/directory1-1") == ['bin.bin']

def test_delete_log_file_doesnt_exist(file_system):
    assert file_system.delete_log_file("/directory/log.log") == False

#-----------------------------td----------------------------------------------------------------

def test_read_log_file_and_append_text_simple_good(file_system_with_files):
    file_system_with_files.append_text("/directory1/directory1-1/log.log", "anything rly")
    assert file_system_with_files.read_log_file("/directory1/directory1-1/log.log") == "anything rly"

def test_read_log_file_several_lines_good(file_system_with_files):
    file_system_with_files.append_text("/directory1/directory1-1/log.log", "anything rly")
    file_system_with_files.append_text("/directory1/directory1-1/log.log", "anything rly part two")
    assert file_system_with_files.read_log_file("/directory1/directory1-1/log.log") == "anything rly\n\ranything rly part two"


def test_read_log_file_doesnt_exist_bad(file_system):
    assert file_system.read_log_file("/directory/log.log") == None

#----------------------------td-----------------------------------------------------------------

def test_append_text_several_lines(file_system_with_files):
    file_system_with_files.append_text("/directory1/directory1-1/log.log", "anything rly\n\ranything rly part two\n\ranything rly comeback")
    assert file_system_with_files.read_log_file("/directory1/directory1-1/log.log") == "anything rly\n\ranything rly part two\n\ranything rly comeback"

def test_append_text_file_doesnt_exist_good(file_system):
    file_system.append_text("/directory/log.log", "anything rly")
    assert file_system.read_log_file("/directory/log.log") == "anything rly"


#-----------------------td---------------------------------------

def test_create_log_file_simple_good(file_system):
    file_system.create_log_file("/directory", "log.log")
    assert file_system.ls("/directory") == ['log.log']

def test_create_log_file_dirs_missing_good(file_system):
    file_system.create_log_file("/directory/directory1/directory2", "log.log")
    assert file_system.ls("/directory/directory1/directory2") == ['log.log']

def test_create_log_file_no_directory_bad():
    fs = FileSystem(5, 5)
    assert fs.create_log_file("/", "log.log") == False

def test_create_log_file_already_exists_bad(file_system_with_files):
    assert file_system_with_files.create_log_file("/directory1/directory1-1", "log.log") == False

def test_create_log_file_impossible_path(file_system):
    assert file_system.create_log_file("/directory/directory.log", "anth.log") == False

def test_create_log_file_dir_is_full_bad(file_system_dir_overflow):
    assert file_system_dir_overflow.create_log_file("/directory1", "anth.log") == False

def test_create_log_file_incorrect_extencion_bad(file_system):
    assert file_system.create_log_file("/directory", "anth.lo") == False


#-------------------------------td!--------------------------------------------------------------

def test_move_log_file_simple_good_1(file_system_with_files):
    file_system_with_files.move_log_file("/directory1/directory1-1/log.log", "/directory1/directory1-three3")
    assert file_system_with_files.ls("/directory1/directory1-1") == ['bin.bin']

def test_move_log_file_simple_good_2(file_system_with_files):
    file_system_with_files.move_log_file("/directory1/directory1-1/log.log", "/directory1/directory1-three3")
    assert file_system_with_files.ls("/directory1/directory1-three3") == ['log.log']

def test_move_binary_file_doesnt_exist(file_system_with_files):
    assert file_system_with_files.move_binary_file("/directory1/directory1-2/bin.bin", "/directory1/directory1-1") == False
    
def test_move_binary_file_overflow(file_system_dir_overflow):
    file_system_dir_overflow.create_binary_file("/directory2", "bin.bin")
    assert file_system_dir_overflow.move_binary_file("/directory2/bin.bin", "/directory1") == False
    

def test_move_binary_file_such_name_already_exists(file_system_with_files):
    file_system_with_files.create_binary_file("/directory1/directory1-2", "bin.bin")
    assert file_system_with_files.move_binary_file("/directory1/directory1-1/bin.bin", "/directory1/directory1-2") == False


