(function(){
    //Bunch of code...
        $(btnAddHover);
        $(initChartContainer);
        $(btnAddSubject);  
})();

 // Setting page: Initialize Chart
function initChartContainer(){
            $('#container').highcharts(
                {
                    chart: {
                        type: 'line'
                    },
                    title: {
                        text: 'Machine Learning Model Statistics'
                    },
                    xAxis: {
                        title: {
                            
                        },
                        categories: ['2017/7/1 00:00:01', '2017/7/1 00:00:01', '2017/7/1 01:02:01', '2017/7/1 06:00:21', '2017/7/1 20:20:00', '2017/7/2 13:23:13', '2017/7/3 10:36:22', '2017/7/4 19:43:02']
                    },
                    yAxis: {
                        title: {
                            text: 'Accuracy of prediction'
                        }
                    },
                    series: [{
                        name: 'Random Forest',
                        data: [43, 60, 73, 79, 84, 86, 87, 88]
                    }, {
                        name: 'Radial Basrs Function Support Vector Classification',
                        data: [55, 70, 82, 87, 89, 91, 92, 92.6]
                    }, {
                        name: 'Multinomial Navie Bayes',
                        data: [60, 63, 65, 66.6, 68, 69, 70.8, 73]
                    }, {
                        name: 'Linear Support Vector Classification',
                        data: [77, 82, 84, 86, 87, 88.8, 89.3, 89.5]
                    }, {
                        name: 'Gaussian Naive Bayes',
                        data: [81, 86, 89.3, 92, 94.5, 95.8, 97, 98.7]
                    }]
                });
        }

// Button Add hover event
function btnAddHover(){
       $("#dropdownMenu1").click(function(){toastr.info('Choose a algorithm model to set it up!');})
}

function btnAddSubject(){
       $("#btnAddSubject").click(function(){toastr.info('Add a new subject...');})
}

function addPseudoClass(){
       $("#btnAddSubject").click(function(){toastr.info('Add a new subject...');})
        css('p:after{content:\'修改一下\'}');
}

function settingPageAddImgBefore(t,s){
    s=document.createElement('style');
    s.innerText=t;
    document.body.appendChild(s);
}
// $(css(".subjectSelection .txtBlur:before{background:url(."{{vm.subject.imageLocation}}") !important}"));



