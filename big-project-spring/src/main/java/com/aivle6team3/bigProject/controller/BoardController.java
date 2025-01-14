package com.aivle6team3.bigProject.controller;

import com.aivle6team3.bigProject.client.api.FastApiClient;
import com.aivle6team3.bigProject.client.dto.NoticeContent;
import com.aivle6team3.bigProject.client.dto.NoticeListResponse;
import com.aivle6team3.bigProject.client.dto.QnaContent;
import com.aivle6team3.bigProject.client.dto.QnaListResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import java.util.List;

@Controller
@RequiredArgsConstructor
@Slf4j
public class BoardController {

    private final FastApiClient fastApiClient;

    // Spring 애플리케이션에서 Spring 서버의 경로
    @GetMapping("/notice")
    public ModelAndView notice_list(@RequestParam(value = "page", defaultValue = "0") int page,
                                    @RequestParam(value = "limit", defaultValue = "10") int limit){

        List<NoticeListResponse> noticeListResponseList = fastApiClient.getNoticeList(page, limit);

        // ModelAndView 객체 생성
        ModelAndView mv = new ModelAndView();

        // 템플릿 이름 설정 (notice.html)
        mv.setViewName("notice");

        // 받은 데이터 전달 (noticeList로 설정)
        mv.addObject("noticeList", noticeListResponseList);

        return mv;
    }

    @GetMapping("/notice/content")
    public ModelAndView read_notice(@RequestParam(value = "id") int id){
        // FastAPI 호출로 데이터 가져오기
        NoticeContent noticeContentResult = fastApiClient.getNoticeContent(id);

        // 데이터를 템플릿에 전달하여 렌더링하기
        ModelAndView mv = new ModelAndView();
        mv.setViewName("notice_page"); // <- templates/notice_page.html 경로를 가리킴
        mv.addObject("readNotice", noticeContentResult);
        return mv;
    }

    // Spring 애플리케이션에서 Spring 서버의 경로
    @GetMapping("/qna")
    public ModelAndView qna_list(@RequestParam(value = "page", defaultValue = "0") int page,
                                    @RequestParam(value = "limit", defaultValue = "10") int limit){

        List<QnaListResponse> qnaListResponseList = fastApiClient.getQnaList(page, limit);

        // ModelAndView 객체 생성
        ModelAndView mv = new ModelAndView();

        // 템플릿 이름 설정 (qna.html)
        mv.setViewName("qna");

        // 받은 데이터 전달 (qnaList로 설정)
        mv.addObject("qnaList", qnaListResponseList);

        return mv;
    }

    @GetMapping("/qna/content")
    public ModelAndView read_qna(@RequestParam(value = "id") int id){

        QnaContent qnaContentResult = fastApiClient.getQnaContent(id);

        ModelAndView mv = new ModelAndView();
        mv.setViewName("qna_page");
        mv.addObject("readQna", qnaContentResult);
        return mv;
    }
}
