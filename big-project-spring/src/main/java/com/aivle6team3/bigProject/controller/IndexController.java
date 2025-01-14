package com.aivle6team3.bigProject.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
@RequiredArgsConstructor
@Slf4j
public class IndexController {

//    private final FastApiClient fastApiClient;

    @GetMapping("/")
    public String root(){
        return "index";
    }

    @GetMapping("/index")
    public String index(){
        return "index";
    }
}
