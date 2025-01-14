package com.aivle6team3.bigProject.client.dto;

import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
public class NoticeContent {
    private int id;
    private String title;
    private String content;
    private int user_id;
    private LocalDateTime created_at;
    private LocalDateTime updated_at;
}
