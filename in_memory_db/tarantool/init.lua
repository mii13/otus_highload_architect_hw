box.cfg {
    listen = 3302;
    memtx_memory = 128 * 1024 * 1024; -- 128Mb
    memtx_min_tuple_size = 16;
    memtx_max_tuple_size = 128 * 1024 * 1024; -- 128Mb
    vinyl_memory = 128 * 1024 * 1024; -- 128Mb
    vinyl_cache = 128 * 1024 * 1024; -- 128Mb
    vinyl_max_tuple_size = 128 * 1024 * 1024; -- 128Mb
    vinyl_write_threads = 2;
    wal_mode = "none";
    wal_max_size = 256 * 1024 * 1024;
    checkpoint_interval = 60 * 60; -- one hour
    checkpoint_count = 6;
    force_recovery = true;

     -- 1 – SYSERROR
     -- 2 – ERROR
     -- 3 – CRITICAL
     -- 4 – WARNING
     -- 5 – INFO
     -- 6 – VERBOSE
     -- 7 – DEBUG
     log_level = 4;
     too_long_threshold = 0.5;
 }

box.schema.user.grant('guest','read,write,execute','universe')

local function create_user_space()
    box.schema.space.create('user', {
        id = 555,
        if_not_exists = true,
        temporary = false
    })

    box.space.user:create_index('primary', {
        type = 'TREE',
        unique = true,
        parts = {1, 'unsigned'},
        if_not_exists = true
    })
    box.space.user:create_index('name_idx', {
        type = 'TREE',
        unique = false,
        parts = {3, 'string'},
        if_not_exists = true
    })
    box.space.user:create_index('second_name_idx', {
        type = 'TREE',
        unique = false,
        parts = {4, 'string'},
        if_not_exists = true
    })

end

function search(name, second_name, limit)
    local cnt = 0
    local result = {}
    for _, tuple in box.space.user.index.name_idx:pairs({name}, { iterator = 'GE' }) do
        if string.startswith(tuple[3], name, 1, -1) and string.startswith(tuple[4], second_name, 1, -1) then
            table.insert(result, tuple)
            cnt = cnt + 1
            if cnt >= limit then
                return result
            end
        end
    end
    return result
end

function search_by_name(name, limit)
    local result = {}
    local cnt = 0
    for _, tuple in box.space.user.index.name_idx:pairs({name}, { iterator = 'GE' }) do
        if string.startswith(tuple[3], name, 1, -1) then
            table.insert(result, tuple)
            cnt = cnt + 1
            if cnt >= limit then
                return result
            end
        end
    end
    return result
end

function search_by_second_name(second_name, limit)
    cnt = 0
    local result = {}
    for _, tuple in box.space.user.index.second_name_idx:pairs({second_name}, { iterator = 'GE' }) do
        if string.startswith(tuple[4], second_name, 1, -1) then
            table.insert(result, tuple)
            cnt = cnt + 1
            if cnt >= limit then
                return result
            end
        end
    end
    return result
end


local function bootstrap()

    if not box.space.mysqldaemon then
        s = box.schema.space.create('mysqldaemon')
        s:create_index('primary',
        {type = 'tree', parts = {1, 'unsigned'}, if_not_exists = true})
    end

    if not box.space.mysqldata then
        t = box.schema.space.create('mysqldata')
        t:create_index('primary',
        {type = 'tree', parts = {1, 'unsigned'}, if_not_exists = true})
    end
    if not box.space.user then
        create_user_space()
    end
end

bootstrap()
