# coding=utf-8
import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options
import pickle

define("port", default=8888, help="run on the given port", type=int)
define("bulk_size", default=6144, help="一次加载多少字", type=int)
define("bookmark_size", default=1024, help="书签没多少个字一个", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        novels = os.listdir(os.path.join(os.path.dirname(__file__), "upload"))
        print(novels)
        self.render("index.html", novels=novels)


class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("uploader.html")

    def post(self):
        file1 = self.request.files["file1"][0]
        original_fname = file1["filename"]
        output_file = open("upload/" + original_fname, "wb")
        output_file.write(file1["body"])
        self.finish("file" + original_fname + " is uploaded")


class Novel(tornado.web.RequestHandler):
    def get(self):
        # 1. 读取书签
        bookmark_fname = os.path.join(os.path.dirname(__file__), "bookmarks.pkl")
        with open(bookmark_fname, "rb") as f:
            bookmarks = pickle.load(f)
        print(bookmarks)

        # 2. 如果是生成页面操作
        # 2.1 获取标题
        title = self.get_argument("title", None)
        if not title:
            self.write("缺少书名")
            return
        f = open(os.path.join(os.path.dirname(__file__), "upload", title))
        content = f.read()

        # 2.2 获取开始位置
        place = int(self.get_argument("place", 0))
        if place == 0:
            place = bookmarks[title]
        print(place)
        part = content[place : place + options.bulk_size]
        parts = []
        for idx in range(0, options.bulk_size, options.bookmark_size):
            parts.append([part[idx : idx + options.bookmark_size], place + idx + options.bookmark_size])
        parts.replace("\n", "<br>")
        self.render("novel.html", parts=parts, title=title)

    def post(self):
        if self.get_argument("action", None) == "bookmark":
            title = self.get_argument("title", None)
            if not title:
                self.write("保存书签，标题不能为空")
                return
            place = int(self.get_argument("place", 0))
            print(place)
            bookmark_fname = os.path.join(os.path.dirname(__file__), "bookmarks.pkl")
            with open(bookmark_fname, "rb") as f:
                bookmarks = pickle.load(f)
            bookmarks[title] = place
            with open(bookmark_fname, "wb") as f:
                pickle.dump(bookmarks, f)
            self.write("success")
            return


class Application(tornado.web.Application):
    def __init__(self):
        # 测试是否有对 当前路径 和 upload路径 的读写权限
        bookmark_fname = os.path.join(os.path.dirname(__file__), "bookmarks.pkl")
        with open(bookmark_fname, "rb") as f:
            records = pickle.load(f)
        print(len(records))
        with open(bookmark_fname, "wb") as f:
            records = pickle.dump(records, f)
        with open("./upload/test.txt", "w") as f:
            print("test", file=f)

        handlers = [(r"/", IndexHandler), (r"/upload", UploadHandler), (r"/novel", Novel)]
        tornado.web.Application.__init__(
            self,
            handlers,
            template_path=os.path.join(
                os.path.dirname(__file__),
                "template",
            ),
            static_path=os.path.join(os.path.dirname(__file__), "upload"),
        )


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
