package com.aivle6team3.bigProject.dto;

import lombok.Getter;
import lombok.Setter;
import org.springframework.cglib.core.Local;

import java.time.LocalDateTime;

// 지금 당장 필요한가? 아닌 것 같은데 일단 바로 지우지 않고 보류
@Getter
@Setter
public class NoticeListDto {
    private int id;
    private String title;
    private String content;
    private int user_id;
    private LocalDateTime created_at;
    private LocalDateTime updated_at;
}
