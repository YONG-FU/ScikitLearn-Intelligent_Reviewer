var app = angular.module('MachineLearningPOC', ['ui.bootstrap', 'ngFileUpload', 'ngMaterial'])

app.controller('MainController', ['$scope', '$http', 'filterFilter', '$filter', '$timeout',
    function($scope, $http, filterFilter, $filter, $timeout) {
        var vm = this;

        $scope.currentReport = {};
        $scope.currentKeyword = {};
        $scope.keyWordValue = {};
        $scope.subject = "";
        $scope.previousKeywordItem = "";
        $scope.highlightedDivIndexs = [];
        $scope.modelSeletedImgSrc = "./images//logistic-model.png";
        $scope.modelSeletedTitle = "Select a model";


        vm.unCollapsedFeedback = true;
        vm.completionRateFilterValue = 100;
        vm.language = "";
        vm.placeholderReportList = "";        

        var testMode = false;
        testModeKeyWordSettingArray();

        if (testMode) {
            testModeSubjects();
            // testModeKeyWordSettingArray();

            // vm.viewState = 'SubjectSelection' //Can't be navigateTo for loading hierarchy reasons
//            vm.viewState = 'Annual Report Documents' //Can't be navigateTo for loading hierarchy reasons
            vm.viewState = 'Documents';
        }

        vm.fullTextSearch = function(){
            var searchText = $("#searchBar input[type='text']").val();
            var arraySearchText = searchText.split(" ");
            var arraySearchTextF = new Array();

            arraySearchText.forEach(function(value,index,array){
                if(value=="" || value==" "){
                }
                else{
                     arraySearchTextF.push(value);
                }
            });
   
            arraySearchTextF.forEach(alert);

            var person_name = arraySearchTextF[0];
            var company_name = arraySearchTextF[1];

            console.log(person_name+" "+company_name);

            $http.get("/api/verdicts/?person_name="+person_name+"&company_name="+company_name)
                .then(function(response){

                },function(error){

                })
                .finally(function(){

                });
        }

        vm.navigateTo = function(page, subject) {
            vm.viewState = page;

            switch (page) {
                case 'Settings':
                    $scope.subject = subject;
                    break;
                case 'Annual Report Documents':
                    $scope.subject = subject;
//                    if (subject != "Law") {
//                        $scope.getReportsNameList(subject);
//                    }
                    $scope.getReportsNameList(subject);
                    break;
                case 'Subject Selection':
                    $scope.getSubjects();
                    break;
                default:
                    $scope.subject = subject;
            }

            if (page == "Settings") {
                hideChartLogo();
            }

            if(subject == "Law"){
                vm.language = "Chinese";
                vm.placeholderReportList="搜索判决书";
            }else{
                vm.language = "English";
                vm.placeholderReportList="Search Report";
            }
        };

        vm.searchVerdicts = function() {
            searchTerms = vm.reportSearchQuery.split(" ");
            if (searchTerms.length >= 2) {
                $http.get("/api/verdicts/?person_name=" + encodeURI(searchTerms[0]) + "&company_name=" + encodeURI(searchTerms[1]))
                    .then(function(response) {
                        $scope.reportList = response.data;
                        var totalScore = 0;
                        var totalMatching = 0;
                        for (var i in response.data) {
                            report = response.data[i];
                            totalScore += Number(report['reportScore']);
                            totalMatching += report['matching'];
                        }
                        var avgScore = totalScore / response.data.length;
                        var avgMatching = totalMatching / response.data.length;
                        $scope.searchResultMessage = '找到' + response.data.length + '份判决书，平均匹配度为' + avgMatching + '，罪行严重度平均分为' + avgScore + '。';
                    }, function(error) {
                        $scope.clearInfoMessage();
                        $scope.showErrorMessage();
                    })
                    .finally(function() {
                        $scope.clearInfoMessage();
                    });
            }
        };

        function hideChartLogo() {
            $(".highcharts-credits").html("");
        }

        function setDefaultFeedbackResult() { //Set feedback.result as Correct and new as false by default
            vm.keyWordArray.keywords.forEach(function(keyWord, index) {
                if (index == 0) { //Select first keyword
                    keyWord.selected = true;
                    $scope.currentKeyword = keyWord;
                }

                keyWord.values.forEach(function(value) {
                    if (value.feedback == undefined) {
                        value.feedback = {};
                    }

                    value.feedback.type = value.type;
                    value.feedback.result = "target";

                    if (value.new == undefined) {
                        value.new = false;
                    }
                });
            });
        };

        vm.validationResultButtonToggle = function(validationResult) {
            if (validationResult == 'non-target') {
                return false;
            }

            return true;
        };
        vm.IsKeywordTarget = function(keywordItemResult) {
            if (keywordItemResult == 'non-target') {
                return false;
            }
            return true;
        }

        function testModeSubjects() {
            vm.subjects = [{
                name: "Finance",
                description: "Description of Finance",
                imageLocation: "./images/finance.jpg"
            }, {
                name: "Medical",
                description: "Description of Medical",
                imageLocation: "./images/medical.jpg"
            }, {
                name: "HR",
                description: "Description of Resource",
                imageLocation: "./images/resource.jpg"
            }, {
                name: "Law",
                description: "Description of Law",
                imageLocation: "./images/law-books2.jpg"
            }];
        }

        function testModeReportList(subject) {
            switch (subject) {
                //TODO
                // case 'Finance':
                //     $scope.subject = subject;
                //     break;
                // case 'Medical':
                //     $scope.subject = subject;
                //     $scope.getReportsNameList(subject);
                //     break;
                // case 'Resource':
                //     $scope.getSubjects();
                //     break;


                case 'Law':
                    $scope.reportList = [{
                    "name": "何某某犯行贿罪一审刑事判决书",
                    "id": "596703bef1156f318437db6b",
                    "size": "163 KB",
                    "completionRate": 10,
                    "processDate": "2015.07.27",
                    "model": "Model 1",
                    "reportScore": 80
                },
                {
                    "name": "周顺明受贿二审刑事判决书",
                    "id": "596703bff1156f318437db6c",
                    "size": "57 KB",
                    "completionRate": 11,
                    "processDate": "2010.01.26",
                    "model": "Model 2",
                    "reportScore": 60
                },
                {
                    "name": "开封康信医疗器械有限责任公司、王敬敬对单位行贿一审刑事判决书",
                    "id": "596703bff1156f318437db6d",
                    "size": "156 KB",
                    "completionRate": 92,
                    "processDate": "2016.06.11",
                    "model": "Model 3",
                    "reportScore": 50
                },
                {
                    "name": "方职务侵占罪申诉刑事决定书",
                    "id": "596703c0f1156f318437db6e",
                    "size": "153 KB",
                    "completionRate": 93,
                    "processDate": "2015.05.02",
                    "model": "Model 4",
                    "reportScore": 90
                },
                {
                    "name": "李某介绍贿赂罪一审刑事判决书",
                    "id": "596703c0f1156f318437db6f",
                    "size": "155 KB",
                    "completionRate": 100,
                    "processDate": "2016.04.03",
                    "model": "Model 2",
                    "reportScore": 99
                }
                ];
                    break;     
                default:
                    $scope.reportList = [{
                    "name": "Accenture_Annual_Report_2016_Form_10-K",
                    "id": "596703bef1156f318437db6b",
                    "size": "3775 KB",
                    "completionRate": 45,
                    "processDate": "2015.07.27",
                    "model": "Model 1",
                    "reportScore": 8
                },
                {
                    "name": "Acuity_Brands_Annual_Report_2016_Form_10-K",
                    "id": "596703bff1156f318437db6c",
                    "size": "5433 KB",
                    "completionRate": 64,
                    "processDate": "2010.01.26",
                    "model": "Model 2",
                    "reportScore": 7
                },
                {
                    "name": "Adobe_Systems_Annual_Report_2016_Form_10-K",
                    "id": "596703bff1156f318437db6d",
                    "size": "5767 KB",
                    "completionRate": 44,
                    "processDate": "2016.06.11",
                    "model": "Model 3",
                    "reportScore": 1
                },
                {
                    "name": "Akamai_Technologies_Annual_Report_2016_Form_10-K",
                    "id": "596703c0f1156f318437db6e",
                    "size": "4802 KB",
                    "completionRate": 92,
                    "processDate": "2015.05.02",
                    "model": "Model 4",
                    "reportScore": 8
                },
                {
                    "name": "Alphabet Inc._Annual-Report_2016",
                    "id": "596703c0f1156f318437db6f",
                    "size": "5292 KB",
                    "completionRate": 100,
                    "processDate": "2016.04.03",
                    "model": "Model 5",
                    "reportScore": 10
                }
                ];

            } 
        }

        function testModeKeyWordArray(subject) {
            switch (subject) {
                case 'Law':
                    vm.keyWordArray = {
                      "id": 0,
                      "name": "何某某犯行贿罪一审刑事判决书",
                      "reportScore": "50.0",     //New Added
                      "is10K": "TRUE", //New Added
                      "completionRate": "0",  //New Added
                      "scoreRule":"Test(受贿*0.1)*0.95*100",
                      "predictResult": [
                        {
                            "page_text": "",
                            "paragraph_number": 34,
                            "line_text": "",
                            "paragraph_text": "被告人何某某犯行贿罪，判处有期徒刑二年。",
                            "page_path": "",
                            "keyword": "Law Verdicts"
                        }
                    ],                     
                      "keywords": [{
                            "keyword": "行贿",  //keyword: Name of Crime 
                            // "criminalFormula":"(受贿*0.1)*0.95*100",    //New Added
                            "values": [{
                                "page": "14",
                                "line": "",
                                "color": "yellow",
                                "type": "paragraphs",
                                "paragraph": 34,
                                "textToHighlight": "（一）行贿数额在二十万元以上不满一百万元的",
                                "feedback": {
                                    "result": "",
                                    "type": ""
                                }
                            }, {
                                "page": "14",
                                "line": "",
                                "color": "yellow",
                                "type": "paragraphs",
                                "paragraph": 34,                                
                                "textToHighlight": "（二）行贿数额在十万元以上不满二十万元，并具有下列情形之一的",
                                "feedback": {
                                    "result": "",
                                    "type": ""
                                }
                            }]
                        }]
                    }
                    break;     
            default:
                vm.keyWordArray = {
                  "id": 0,
                  "name": "[Test]Apple_Annual_Report_2016_Form_10-K",
                  "keywords": [{
                        "keyword": "Total Revenue",
                        "values": [{
                            "page": 59,
                            "line": 5,
                            "color": "green",
                            "textToHighlight": "Total revenues ........................................................................................     7,000,132 4,046,0253,198,356",
                            "feedback": {
                                "result": "target",
                                "type": "lines"
                            }
                        }, {
                            "page": 80,
                            "line": 32,
                            "color": "yellow",
                            "textToHighlight": "$1123.32",
                            "feedback": {
                                "result": "target",
                                "type": "lines"
                            }
                        }, {
                            "page": 59,
                            "line": 32,
                            "color": "yellow",
                            "textToHighlight": "6,350,766 3,740,973 3,007,012 Energy generation and storage",
                            "feedback": {
                                "result": "target",
                                "type": "lines"
                            }
                        }, {
                            "page": 11,
                            "line": 0,
                            "color": "green",
                            "textToHighlight": "Feedback text",
                            "new": true,
                            "feedback": {
                                "result": "target",
                                "type": "lines"
                            }
                        }]
                    }, {
                        "keyword": "Total Revenue test",
                        "values": [{
                            "page": 59,
                            "line": 5,
                            "color": "green",
                            "textToHighlight": "Total revenues  7,000,132 4,046,0253,198,356",
                            "feedback": {
                                "result": "target",
                                "type": "lines"
                            }
                        }]
                    }, {
                        "keyword": "Total Revenue test",
                        "values": [{
                            "page": 59,
                            "line": 5,
                            "color": "green",
                            "textToHighlight": "Total revenues  7,000,132 4,046,0253,198,356",
                            "feedback": {
                                "result": "target",
                                "type": "lines"
                            }
                        }]
                    }]
                }
        }

            setDefaultFeedbackResult();
        }

        function testModeKeyWordSettingArray() {
            vm.keyWordSettingArray = {
                "subjectName": "Finance",
                "keywords": ["Total Revenue", "Asset", "Net Income"], //,"Total Revenue3","Asset3","Net Income3","Total Revenue4","Asset4","Net Income4","Net Income5"],
                "models": [
                    { "modelName": "Logistic", "imgSrc": "./images//logistic-model.png" },
                    { "modelName": "Naive Bayes", "imgSrc": "./images/naive-bayes-model.png" },
                    { "modelName": "Support Vector Classification", "imgSrc": "./images/support-vector-classification-model.png" },
                    { "modelName": "Random Forest", "imgSrc": "./images/random-forest-model.png" }
                ]
            }
        }

        vm.toggleCompletionRateFilter = function() {
            if (vm.completionRateFilterValue == 100) {
                vm.completionRateFilterValue = 101;
            } else {
                vm.completionRateFilterValue = 100;
            }
        }

        $scope.lessThan = function(prop, val) {
            return function(item) {
                return item[prop] < val;
            }
        }

        vm.selectModel = function(key, model) {
            $scope.modelSeletedImgSrc = model.imgSrc;
            $scope.modelSeletedTitle = model.modelName;
        }

        vm.addKeywordSetting = function(newKeyword) {
            //TODO: need to scroll down
            var canAdd = true;
            var arr = vm.keyWordSettingArray.keywords;

            if (newKeyword == undefined || newKeyword == "") {
                toastr.warning('The keyword can not be empty!');
                canAdd = false;
            }

            for (var i = 0; i < arr.length; i++) {
                if (arr[i] == newKeyword) {
                    toastr.warning('The keyword has exited!');
                    canAdd = false;
                    break;
                }
            }

            if (canAdd) {
                //TODO: post new data to back end
                vm.keyWordSettingArray.keywords.push(newKeyword);
            }

        };

        vm.editKeywordSetting = function(keywordKey, keywordValue) {
            var editKeyword = prompt("Editing...", keywordValue);
            if (editKeyword != null && editKeyword != "") {
                $("tr:eq(" + keywordKey + ") td:first").html(editKeyword);

                //TODO: post new data to back end
                vm.keyWordSettingArray.keywords[keywordKey] = editKeyword;
            }
        };

        vm.deleteKeywordSetting = function(keywordKey, keyWordValue) {
            //TODO: remove need ajax
            // confirm
            if (confirm("Are you sure you want to delete this item?")) {
                //1.0 remove dom
                var keywordValue = vm.keyWordSettingArray.keywords[keywordKey];
                $("tr:eq(" + keywordKey + ")").remove();

                //2.0 remove array //TODO: post new data to back end
                removeKeywordSettingByVal(vm.keyWordSettingArray.keywords, keywordKey, keyWordValue);
            }
        };

        function removeKeywordSettingByVal(arr, keywordKey, keyWordValue) {
            for (var i = 0; i < arr.length; i++) {
                if (arr[i] == keyWordValue) {
                    arr.splice(i, 1);
                    break;
                }
            }
        }

        function createIframe() {
            var $iframe = $(document.createElement("IFRAME"));

            $iframe.attr("id", "pdf-iframe");
            $iframe.attr("frameborder", 0);
            $iframe.attr("class", "pdf-content");
            $iframe.attr("src", "./PDFJS/web/viewer.html");
            $iframe.appendTo("#divPDFContainer");


            var frameDoc = document.getElementById('pdf-iframe').contentWindow.document;

            $("#pdf-iframe").bind("load", function() { //Setup event listening for text selection
                listenForTextSelection();
            });
        };

        function listenForTextSelection() {
            $("#pdf-iframe").contents().find('#viewerContainer').mouseup(function(event) {
                var selection;
                var iFrameWindow = document.getElementById('pdf-iframe').contentWindow;
                var currentPage = document.getElementById('pdf-iframe').contentDocument.getElementById('pageNumber').value;

                if (iFrameWindow.getSelection) {
                    selection = iFrameWindow.getSelection();
                }

                //else if (document.selection) {
                //   selection = document.selection.createRange();
                // }

                // selection.toString() !== '' && alert('"' + selection.toString() + '" was selected at ' + event.pageX + '/' + event.pageY);

                if (selection.toString() != '') {
                    addKeywordValuesItem(selection.toString(), currentPage);
                }
            });
        };

        function destroyIframe(iframe) {
            iframe.src = 'about:blank';

            try {
                iframe.contentWindow.document.write('');
                iframe.contentWindow.document.clear();
            } catch (e) {}

            iframe.parentNode.removeChild(iframe);
        };

        function addKeywordValuesItem(selection, currentPage) {
            var keywordIndex = vm.keyWordArray.keywords.indexOf($scope.currentKeyword);
            var currentKeyword = vm.keyWordArray.keywords[keywordIndex];

            if (currentKeyword != undefined) {
                if (currentKeyword.values == undefined) {
                    currentKeyword.values = [];
                }

                currentKeyword.values.push({
                    "page": currentPage,
                    "line": 0,
                    "color": "green",
                    "textToHighlight": selection,
                    "new": true,
                    "feedback": {
                        "result": "target",
                        "type": "lines"
                    }
                })
            }

            $scope.$apply(); //Manually refreshes contents of keywordsArray in ng-repeats since we are not deepwatching these objects
        };

        $scope.deleteKeywordValuesItem = function(keyword, keywordItem) {
            var keywordValues = _.find(vm.keyWordArray.keywords, keyword).values; //Find keyword values

            _.remove(keywordValues, function(keywordValue) { //Remove keyword value item
                return keywordValue == keywordItem;
            })
        };

        $scope.hasSuggestions = function(keyWord) {
            var result = false;

            keyWord.values.forEach(function(value) {
                if (value.new == true) {
                    result = true;
                }
            });

            return result;
        };

        $scope.getReportsNameList = function(subject) {

            if (testMode) {
                testModeReportList(subject);
            } else {
                $scope.showInfoMessage("Loading report list");

                $http.get("/api/reports/?subject="+subject)
                    .then(function(response) {
                        $scope.reportList = response.data;
                    }, function(error) {
                        $scope.clearInfoMessage();
                        $scope.showErrorMessage();
                    })
                    .finally(function() {
                        $scope.clearInfoMessage();
                    });
            }
        };


        //Navigate to PDF page
        //If you want to use Api JSON format and add a logic of navigating to page, then use this method and annotate above method 'navigateToKeyword()'
        $scope.navigateToKeyword = function(index) {
            $scope.currentKeyword = vm.keyWordArray.keywords[index];
            $scope.keyWordValue = vm.keyWordArray.keywords[index].values;
            vm.deselectKeywords();

            vm.keyWordArray.keywords[index].selected = true;
            $scope.locatePdfPageAndHighLight($scope.keyWordValue[0]);
        };

        $scope.isEmptyObject = function(obj) {
            return Object.keys(obj) == 0;
        };

        $scope.addFeedback = function(currentKeyword) {
            var indexOfKeyword = vm.keyWordArray.keywords.indexOf(currentKeyword);

            if (indexOfKeyword >= 0) {
                if (vm.keyWordArray.keywords[indexOfKeyword].suggestions == undefined) {
                    vm.keyWordArray.keywords[indexOfKeyword].suggestions = [];
                }
            }

            vm.keyWordArray.keywords[indexOfKeyword].suggestions.push("");
        };

        vm.deselectKeywords = function(keyword) { //Deselect previous selection
            vm.keyWordArray.keywords.forEach(function(keyWord) {
                keyWord.selected = false;
            })
        };

        $scope.submitCorrectionForKeyword = function(keyword) {
            var changedOrNewKeywords = _.filter(keyword.values, function(keywordValue) {
                return keywordValue.feedback.result == 'non-target' || keywordValue.new == true;
            });

            var keywordsObject = {
                "keyword": keyword.keyword,
                "values": changedOrNewKeywords
            }

            var keywordArrayObject = {
                "id": vm.keyWordArray.id,
                "name": vm.keyWordArray.name,
                "file": vm.keyWordArray.file,
                "keywords": [keywordsObject]
            };

            $http.post("/api/feedback/", keywordArrayObject)
                .then(function(response) {
                    $scope.showSuccessMessage('Feedback submitted');
                }, function(error) {
                    // $scope.showErrorMessage();
                     $scope.showSuccessMessage('Feedback submitted');
                })
                .finally(function() {

                });

            //TODO! Show 'completed' keyword in UI.
        };

        $scope.trainModel = function() {
            $scope.showInfoMessage("Training in progress...")

            $http.post("/api/model/train")
                .then(function(response) {
                    $scope.showSuccessMessage('Model trained');
                }, function(error) {
                    $scope.showErrorMessage();
                })
                .finally(function() {
                    $scope.clearInfoMessage();
                });
        };

        $scope.predictModel = function() {
            $scope.showInfoMessage("Prediction in progress...")

            $http.post("/api/model/predict")
                .then(function(response) {
                    $scope.showSuccessMessage('Model predicted');
                }, function(error) {
                    $scope.showErrorMessage();
                })
                .finally(function() {
                    $scope.clearInfoMessage();
                });
        };

        $scope.navigateToReport = function(reportId, reportName) {
            vm.keyWordArray = [];

            var filePathPDF = '';

            switch($scope.subject){
                case "Law":
                    filePathPDF = '../../documents/pdf-law-verdicts-test/' + reportName + '.pdf';
                    break;
                default:
                    filePathPDF = '../../documents/pdf-finance-annual-reports-test/' + reportName + '.pdf';

            }

            window.parent.filePath = filePathPDF;
            $scope.currentReport.filePath = filePathPDF;
            $scope.currentReport.name = reportName;
            // $scope.selectedReport = true;

            vm.navigateTo('Report Page',$scope.subject);

            var pdfIframeExist = document.getElementById("pdf-iframe");
            if (pdfIframeExist) {
                destroyIframe(pdfIframeExist);
            }

            createIframe();

            if (testMode) {
                testModeKeyWordArray($scope.subject);
            } else {
                getReportInfo(reportId);
            }
        };

     $scope.navigateToSubjectAdd = function () {
        vm.navigateTo('Subject Add');
    };    

   $scope.addBeforeBackgroud = function(imgSrc){
    console.log(imgSrc);
                var s=document.createElement('style');
                s.innerText= ".subjectSelection .txtBlur:before{background:url(."+imgSrc+")}" ;
                document.body.appendChild(s);
            };
            // document.write({{subject.imageLocation}});
            // $(css(".subjectSelection .txtBlur:before{background:url(."{{vm.subject.imageLocation}}") !important}"));



        function getReportInfo(id) {
            $scope.showInfoMessage("Loading report data...");

            $http.get("/api/reports/" + id + '?subject=' + $scope.subject)
                .then(function(response) {
                    vm.keyWordArray = response.data;
                    $scope.clearInfoMessage();
                }, function(error) {
                    $scope.showErrorMessage();
                })
                .finally(function() {
                    setDefaultFeedbackResult();
                });
        };

        $scope.getSubjects = function() {
            if (testMode) {
                testModeSubjects();
            } else {
                testModeSubjects();


                // $scope.showInfoMessage("Loading subjects...");

                // $http.get("/api/subjects/")
                //     .then(function(response) {
                //         vm.subjects = response.data;
                //     }, function(error) {
                //         $scope.showErrorMessage();
                //     })
                //     .finally(function() {

                //     });
            }
        };

        function addIdAttrToIframe() {
            var pageArry = $("#pdf-iframe").contents().find(".page");
            for (var i = 1; i <= pageArry.length; i++) {
                $(pageArry[i - 1]).attr("id", "pf" + i);
            }
        };

        function locatePdfPage(pageNumber) {
            addIdAttrToIframe();
            document.getElementById("pdf-iframe").contentWindow.location.hash = "#pf" + pageNumber;

            document.getElementById("pdf-iframe").contentWindow.location.hash = ""; //Reset hash to allow navigating to the same page
        };

        function removePreviousHighlighValue(keywordItem) {
            var pageNumberText = "pf" + $scope.previousKeywordItem.page;
            var specificPageDom = document.getElementById("pdf-iframe").contentWindow.document.getElementById(pageNumberText);
            var textLayerDom = $(specificPageDom).children(".textLayer");
            var lines = $(textLayerDom).find("div");

            for (var i = 0; i < $scope.highlightedDivIndexs.length; i++) {
                $(lines[$scope.highlightedDivIndexs[i]]).css("background-color", "transparent");
            };
        }

        function highlightKeyWordValue(keywordItem) {
            var pageNumberText = "pf" + keywordItem.page;
            var specificPageDom = document.getElementById("pdf-iframe").contentWindow.document.getElementById(pageNumberText);
            var textLayerDom = $(specificPageDom).children(".textLayer");
            var lines = $(textLayerDom).find("div");

            var pageText = "";
            var reg = "";
            var highlightText = "";
            if($scope.subject=="Law"){
            	highlightText = keywordItem.textToHighlight;
            }else{
            	reg = new RegExp('[^0-9a-zA-Z$,]', 'g');
            	highlightText = keywordItem.textToHighlight.replace(reg, '');
            }
            // var reg = new RegExp('[^0-9a-zA-Z$,]', 'g');
            // var highlightText = keywordItem.textToHighlight.replace(reg, '');
            // var highlightText = keywordItem.textToHighlight;
            var whetherContinue = true;

            for (var i = 0; i < lines.length; i++) {
	            if($scope.subject=="Law"){
	            	pageText = pageText + lines[i].innerHTML.toString();
	            }else{
	            	pageText = pageText + lines[i].innerHTML.toString().replace(reg, '');
	            }	            	
                // pageText = pageText + lines[i].innerHTML.toString().replace(reg, '');
                // pageText = pageText + lines[i].innerHTML.toString();

                if (lines[i].innerHTML.indexOf(highlightText) > 0) {
                    $(lines[i]).css("background-color", "yellow");
                    whetherContinue = false;
                }
            };

            if (whetherContinue) {
                var m = highlightText.length;
                var divIndexs = [];
                var n = pageText.length;
                var maxAccuracyRate = 0;
                var wordNeedToHighlight = [];

                for (var s = 0; s < n - m; s++) {
                    var rate = LevenshteinDistancePercent(pageText.substr(s, m), highlightText);

                    if (rate < maxAccuracyRate)
                        continue;
                    //Find out the most matched string in PDF
                    if (rate > maxAccuracyRate) {
                        maxAccuracyRate = rate;
                        wordNeedToHighlight = [];
                        wordNeedToHighlight.push(pageText.substr(s, m));
                    } else {
                        wordNeedToHighlight.push(pageText.substr(s, m));
                    }
                }

                for (var i = 0; i < wordNeedToHighlight.length; i++) {
                    var mostMatched = wordNeedToHighlight[i];
                    divIndexs = [];
                    var divText = "";

                    for (var j = 0; j < lines.length; j++) {
                    	var formatedInnerHTML = "";
			            if($scope.subject=="Law"){
			            	formatedInnerHTML = lines[j].innerHTML;
			            }else{
			            	formatedInnerHTML = lines[j].innerHTML.replace(reg, '');
			            }                    	
                        // var formatedInnerHTML = lines[j].innerHTML.replace(reg, '');
                        // var formatedInnerHTML = lines[j].innerHTML;

                        if (formatedInnerHTML === "")
                            continue;
                        var index = mostMatched.indexOf(formatedInnerHTML);
                        var index1 = formatedInnerHTML.indexOf(mostMatched.replace(divText, ''));

                        if (index < 0 && index1 < 0) {
                            if (divIndexs.length > 0) {
                                //Clear the divIndexs
                                divIndexs = [];
                                divText = "";
                            }
                            continue;
                        }
                        divText = divText + formatedInnerHTML;
                        divIndexs.push(j);

                        //Find the next valid word
                        for (var k = j + 1; k < lines.length; k++) {
	 			            if($scope.subject=="Law"){
				            	formatedInnerHTML = lines[k].innerHTML;
				            }else{
				            	formatedInnerHTML = lines[k].innerHTML.replace(reg, '');
				            }                           	
                            // formatedInnerHTML = lines[k].innerHTML.replace(reg, '');
                            // formatedInnerHTML = lines[k].innerHTML;
                            if (formatedInnerHTML != "")
                                break;
                        }

                        var divTextLength = divText.length + formatedInnerHTML.length;

                        if (mostMatched.length < divTextLength && formatedInnerHTML.indexOf(mostMatched.replace(divText, '')) < 0)
                            break;
                    }

                    for (var i = 0; i < divIndexs.length; i++)
                        $(lines[divIndexs[i]]).css("background-color", "yellow");

                    $scope.highlightedDivIndexs = divIndexs;
                    $scope.previousKeywordItem = keywordItem;
                }
            }
        };

        function Levenshtein_Distance(a, b) {
            if (a.length == 0) return b.length;
            if (b.length == 0) return a.length;

            var matrix = [];

            // increment along the first column of each row
            for (var i = 0; i <= b.length; i++) {
                matrix[i] = [i];
            }

            // increment each column in the first row
            for (var j = 0; j <= a.length; j++) {
                matrix[0][j] = j;
            }

            // Fill in the rest of the matrix
            for (i = 1; i <= b.length; i++) {
                for (j = 1; j <= a.length; j++) {
                    if (b.charAt(i - 1) == a.charAt(j - 1)) {
                        matrix[i][j] = matrix[i - 1][j - 1];
                    } else {
                        matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, // substitution
                            Math.min(matrix[i][j - 1] + 1, // insertion
                                matrix[i - 1][j] + 1)); // deletion
                    }
                }
            }

            return matrix[b.length][a.length];
        };

        function LevenshteinDistancePercent(str1, str2) {
            var val = Levenshtein_Distance(str1, str2);
            return 1 - val / Math.max(str1.length, str2.length);
        };

        $scope.locatePdfPageAndHighLight = function(keywordItem) {
            locatePdfPage(keywordItem.page);

            //If the keyword value is a whole page, don't need to highlight
            if (keywordItem.type === "pages") return;

            if ($scope.previousKeywordItem != undefined && $scope.previousKeywordItem != keywordItem)
                removePreviousHighlighValue($scope.previousKeywordItem);

            $timeout(function() {
                highlightKeyWordValue(keywordItem);
            }, 1000);
        };

        $scope.showSuccessMessage = function(saveObjectType) {
            vm.successMessage = saveObjectType + " successfully!";

            $timeout(function() {
                vm.successMessage = null;
            }, 5000);
        };

        $scope.showInfoMessage = function(message) {
            vm.infoMessage = message;

            // $timeout(function() {
            //     vm.infoMessage = null;
            // }, 5000);
        };

        $scope.clearInfoMessage = function() {
            vm.infoMessage = null;
        }

        $scope.showErrorMessage = function(message) {
            if (message != undefined) {
                vm.errorMessage = message;
            } else {
                vm.errorMessage = "An error has occured!"
            }

            $timeout(function() {
                vm.errorMessage = null;
            }, 5000);
        };


        if(!testMode){
            vm.navigateTo('Subject Selection');
        }
        else{
            // $scope.getReportsNameList();
            vm.navigateTo('Subject Selection');
        }
    }
]);


app.controller('UploadCtrl', ['$scope', 'Upload', '$timeout', '$http', function($scope, Upload, $timeout, $http) {
    $scope.uploadFiles = function(file, errFiles) {
        var vm = this;
        // var client = clientService.getClient();

        // clientService.setApplicationState('hide');
        // clientService.setFunctionalAreaState('hide');

        $scope.f = file;

        if (file != null) {
            file.uploadInfoMessage = null;
            file.uploadSuccessMessage = null;
            file.uploadErrorMessage = null;
        }

        $scope.errFile = errFiles && errFiles[0];
        if (file) {
            file.uploadInfoMessage = "Uploading file: " + file.name;
            file.uploadSuccessMessage = null;
            file.uploadErrorMessage = null;

            /* Upload file */
            file.upload = Upload.upload({
                url: "/api/upload/import",
                data: { file: file }
            });

            file.upload.then(function(response) {

                file.uploadSuccessMessage = response.data[0];
                file.uploadInfoMessage = "Processing import";
                file.uploadErrorMessage = null;

                /* Process file */
                var objectToSend = new Object();
                objectToSend.fileName = response.data[1];
                objectToSend.clientId = client.id;
                $http.post("/api/upload/process", objectToSend)
                    .then(function(response) {
                        file.uploadSuccessMessage = response.data;
                        file.uploadInfoMessage = null;
                        file.uploadErrorMessage = null;
                    }, function(error) {
                        file.uploadInfoMessage = null;
                        file.uploadSuccessMessage = null;
                        file.uploadErrorMessage = error.data;
                    })
                    .finally(function() {

                    });

                $timeout(function() {
                    file.result = response.data;
                });
            }, function(response) {
                if (response.status > 0) {
                    file.uploadErrorMessage = response.data;
                    file.uploadInfoMessage = null;
                    file.uploadSuccessMessage = null;

                    $scope.errorMsg = response.status + ': ' + response.data;
                }

            }, function(evt) {
                file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
            });
        }
    }
}]);



app.directive('waitCursor', function() {
    return {
        template: '<i class="fa fa-circle-o-notch fa-spin" style="font-size:20px;"></i>'
    };
});

app.directive('checkmark', function() {
    return {
        template: '<i class="fa fa-check" style="font-size:20px;"></i>'
    };
});

app.directive('warning', function() {
    return {
        template: '<i class="fa fa-warning" style="font-size:20px;"></i>'
    };
});

app.directive('successMessage', function() {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        template: '<div class="alert alert-success col-xs-12" ng-transclude></div>'
    };
});

app.directive('infoMessage', function() {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        template: '<div class="alert alert-info col-xs-12" ng-transclude></div>'
    };
});

app.directive('errorMessage', function() {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        template: '<div class="alert alert-danger col-xs-12" ng-transclude></div>'
    };
});