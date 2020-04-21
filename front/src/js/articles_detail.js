
function ArticlesList() {

}

ArticlesList.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#comment-btn');
    var textarea = $("textarea[name='comment']");
    submitBtn.click(function () {
        var content = textarea.val();
        var articles_id = submitBtn.attr('data-articles-id');

        blogajax.post({
            'url': '/articles/comment/',
            'data': {
                'content': content,
                'articles_id': articles_id
            },
            'success': function (result) {
                if (result['code'] === 200 ) {
                    var comment = result['data'];
                    var tpl = template('comment-item', {"comment": comment});
                    var commentListGroup = $(".comment-list");

                    window.messageBox.showSuccess('评论发表成功！');
                    textarea.val("");
                    setTimeout(function(){window.location = window.location.pathname;},500);
                    //setTimeout(function(){commentListGroup.prepend(tpl);},100);
                    //window.location = window.location.href;
                } else {
                    window.messageBox.showError(result['message']['content']);//('评论内容不能为空');//
                }
            }
        });
    });
};



ArticlesList.prototype.run = function () {
    this.listenSubmitEvent();
};


$(function () {
    var articlesList = new ArticlesList();
    articlesList.run();
});