(module
  (memory (export "memory") 1 )
  (func (export "check_flag") (result i32)
    i32.const 0x7b
    i32.const 38
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x67
    i32.const 20
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x5f
    i32.const 46
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x21
    i32.const 3
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x63
    i32.const 18
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x6e
    i32.const 119
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x5f
    i32.const 51
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x79
    i32.const 59
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x34
    i32.const 9
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x57
    i32.const 4
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x35
    i32.const 37
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x33
    i32.const 12
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x62
    i32.const 111
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x63
    i32.const 45
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x7d
    i32.const 97
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x30
    i32.const 54
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x74
    i32.const 112
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x31
    i32.const 106
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x66
    i32.const 43
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x34
    i32.const 17
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x34
    i32.const 98
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x54
    i32.const 120
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x5f
    i32.const 25
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x6c
    i32.const 127
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 0x41
    i32.const 26
    call $stir
    i32.load8_u
    i32.ne
    if
      i32.const 0
      return
    end

    i32.const 1
    return
  )

  (func $stir (param $x i32) (result i32)
    i32.const 1024
    i32.const 23
    i32.const 37
    local.get $x
    i32.const 0x5a5a
    i32.xor
    i32.mul
    i32.add
    i32.const 101
    i32.rem_u
    i32.add
    return
  )
)
