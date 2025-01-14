package com.aivle6team3.bigProject.client.dto;

import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
public class QnaContent {
    private int id;
    private String title;
    private String content;
    private int user_id;
    private LocalDateTime created_at;
    private LocalDateTime updated_at;
    private int reply_user;
    private String reply_title;
    private String reply_content;
//    private LocalDateTime reply_at;
}
