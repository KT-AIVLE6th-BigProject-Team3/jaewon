package com.aivle6team3.bigProject.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.*;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "notice")
public class NoticeList {

    @Id
    @Column(name = "id", nullable = false)
    private int notice_id;

    @Column(name = "title", nullable = false)
    private String title;

    @Column(name = "created_at", nullable = false)
    private String date;

//    @Column(name = "writer_id", nullable = false)
//    private String "writer_id";
//
//    @Column(name = "content", nullable = false)
//    private String "content";
}
