package com.aivle6team3.bigProject.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class NoticeListDto {
    private int notice_id;
    private String title;
    private String date;
    private String writer_id;
    private String content;
}
