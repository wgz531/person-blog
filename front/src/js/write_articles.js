function Articles() {
    this.progressGroup = $("#progress-group");
}

Articles.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor',{
        'initialFrameHeight': 400,
        'initialFrameWidth':'100%',
        'serverUrl': '/ueditor/upload/'
    });
};



Articles.prototype.listenSubmitEvent = function () {
    var submitBtn = $("#submit-btn");
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-articles-id');
        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var content = window.ue.getContent();
        console.log(category);

        var url = '';
        if(pk){
            url = '/cms/edit_articles/';
        }else{
            url = '/cms/write_articles/';
        }

        blogajax.post({
            'url': url,
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'content': content,
                'pk': pk
            },
            'success': function (result) {
                if(result['code'] === 200){
                    blogalert.alertSuccess('恭喜！新闻发表成功！',function () {
                        window.location.replace('/cms/articles_list/');
                    });
                }
            }
        });
    });
};

Articles.prototype.run = function () {
    var self = this;
    self.initUEditor();
    self.listenSubmitEvent();
    // self.listenUploadFielEvent();
};


$(function () {
    var articles = new Articles();
    articles.run();

   Articles.progressGroup = $('#progress-group');
});