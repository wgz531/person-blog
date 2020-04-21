
function Index() {
    var self = this;
    self.page = 2;
    self.category_id = 0;
    self.loadBtn = $("#load-more-btn");
}

Index.prototype.listenLoadMoreEvent = function () {
    var self = this;
    var loadBtn = $("#load-more-btn");
    var s = $('#s');
    loadBtn.click(function () {
        var keywords = s.attr('data-kw').toString();
        console.log(keywords);
        blogajax.get({
            'url': '/articles/list/',
            'data':{
                'keywords':keywords,
                'p': self.page,
                'category_id': self.category_id
            },
            'success': function (result) {
                if(result['code'] === 200){
                    var articles = result['data'];
                    if(articles.length > 0){
                        var tpl = template("articles-item",{"articles":articles});
                        var ul = $(".list-inner-group");
                        ul.append(tpl);
                        self.page += 1;
                    }else{
                        loadBtn.hide();
                    }
                }
            }
        });
    });
};

Index.prototype.listenCategorySwitchEvent = function () {
    var self = this;
    var tabGroup = $(".list-tab");
    var s = $('#s');
    tabGroup.children().click(function () {
        var keywords = s.attr('data-kw');
        // this：代表当前选中的这个li标签
        var li = $(this);
        var category_id = li.attr("data-category");
        var page = 1;
        blogajax.get({
            'url': '/articles/list/',
            'data': {
                'keywords':keywords,
                'category_id': category_id,
                'p': page
            },
            'success': function (result) {
                if(result['code'] === 200){
                    var articles = result['data'];
                    var tpl = template("articles-item",{"articles":articles});
                    // empty：可以将这个标签下的所有子元素都删掉
                    var articlesListGroup = $(".list-inner-group");
                    articlesListGroup.empty();
                    articlesListGroup.append(tpl);
                    self.page = 2;
                    self.category_id = category_id;
                    li.addClass('active').siblings().removeClass('active');
                    self.loadBtn.show();
                }
            }
        });
    });
};

Index.prototype.run = function () {
    var self = this;
    self.listenLoadMoreEvent();
    self.listenCategorySwitchEvent();
};

$(function () {
    var index = new Index();
    index.run();
});