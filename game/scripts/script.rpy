# 遊戲腳本位於此檔案。

# ── 初始化 bridge ──────────────────────────────────────────────────
init python:
    import sys, os
    sys.path.insert(0, os.path.join(renpy.config.gamedir, "..", "bridge"))
    import bridge
    bridge.init()

# ── 角色定義 ───────────────────────────────────────────────────────
define n = Character("旁白", color="#1f2b50")
define p = Character("林宇凡", color="#1f2b50")
define l = Character("林正雄", color="#000000",)
define g = Character("管理員", color="#1f2b50")
define s = Character("王子騫", color="#1f2b50")
define o = Character("服務生", color="#1f2b50")

# ── 圖片初始化 ─────────────────────────────────────────────────────
image old_house_room:
    "images/old_house_room.png"
    zoom 1.15

image bookshelfs:
    "images/bookshelfs.png"
    zoom 0.32

image m1:
    "images/m1.png"
    zoom 0.9
    xanchor 0.9
    yanchor 0.9
    xpos 1800
    ypos 1000

image officer:
    "images/officer.png"
    zoom 0.9
    xanchor 0.9
    yanchor 0.9
    xpos 500
    ypos 1000

image map:
    "images/map.png"
    xpos 1050

image q1:
    "images/q1.png"
    zoom 0.55
    xanchor 0.55
    yanchor 0.55
    xpos 1010
    ypos 400

image q2:
    "images/q2.png"
    zoom 0.55
    xanchor 0.55
    yanchor 0.55
    xpos 1010
    ypos 400

image q3:
    "images/q3.png"
    zoom 0.55
    xanchor 0.55
    yanchor 0.55
    xpos 1010
    ypos 400

image q4:
    "images/q4.png"
    zoom 0.55
    xanchor 0.55
    yanchor 0.55
    xpos 1010
    ypos 400

# ── 謎題輸入畫面 ───────────────────────────────────────────────────
screen puzzle_input(puzzle_index, elapsed_sec):
    modal True

    frame:
        xalign 0.5
        yalign 0.85
        xsize 700
        padding (30, 20)

        vbox:
            spacing 15

            # 已解鎖的提示
            python:
                hints = []
                for i in range(3):
                    h = bridge.get_hint(puzzle_index, elapsed_sec, i)
                    if h:
                        hints.append(h)

            if hints:
                text "提示：" color "#aaaaaa" size 22
                for hint_text in hints:
                    text "• [hint_text]" color "#cccccc" size 20

            # 輸入框
            text "請輸入答案：" color "#ffffff" size 24
            input:
                id "ans"
                value ScreenVariableInputValue("user_input")
                xmaximum 400
                color "#ffffff"
                size 24

            # 確認按鈕
            textbutton "確認":
                xalign 0.5
                action Return()

# ── 通用謎題函式 ───────────────────────────────────────────────────
init python:
    import time

    def do_puzzle(puzzle_index):
        """
        呼叫此函式來處理謎題輸入與驗證。
        回傳花費秒數。
        """
        start = time.time()
        while True:
            elapsed = int(time.time() - start)
            renpy.call_screen("puzzle_input",
                              puzzle_index=puzzle_index,
                              elapsed_sec=elapsed)
            user_input = renpy.get_screen("puzzle_input") and "" or ""
            # 從 screen variable 取得輸入
            ans = renpy.python.store._last_ans if hasattr(renpy.python.store, "_last_ans") else ""
            if bridge.check_answer(puzzle_index, ans):
                elapsed = int(time.time() - start)
                bridge.save_result(puzzle_index, elapsed, 0)
                return elapsed
            else:
                renpy.say(None, "答案不對，再試試看。")


# ── 遊戲開始 ───────────────────────────────────────────────────────
label start:

    scene black
    with fade

    n "祖父林正雄過世後的第三天，你回到久未整理的老家。"
    n "房間裡還留著舊木櫃的氣味，午後的光從半掩的窗簾縫隙斜斜落下，照亮空氣裡漂浮的灰塵。"

    scene old_house_room
    with dissolve
    show m1

    n "你原本只是想把遺物分門別類，卻在最角落的櫃子裡，拖出了一只泛黃的舊皮箱。"
    n "皮箱的皮面已經裂開，金屬扣環微微生鏽，像是很久很久以前，就沒有人再碰過它。"

    p "……這是什麼？"

    hide m1
    show envolope:
        ypos -150
    with dissolve

    n "你打開皮箱。裡面沒有值錢的東西，只有幾張舊照片、一疊泛黃紙張，和一封沒有寄出的信。"
    n "信封上只寫著名字：林正雄。"
    n "筆跡很工整，卻像是被什麼壓抑著，連收信人都沒有寫完。"

    hide envolope
    show envolope1
    with dissolve

    n "你抽出信紙，紙張薄得像會在手中碎掉。"
    n "那是一封寫於 1960 年的信。"
    n "而信的背面，還藏著一張手繪的基隆地圖。"

    hide envolope1
    show map:
        xpos 100
    with dissolve

    n "地圖上標了四個地點。"
    n "舊郵局、報社舊址、燈塔、白米甕砲台。"
    n "每一個點旁邊都畫了小小的記號，像是某段回憶被刻意留下的路標。"

    show m1
    with dissolve
    p "這些地方……祖父去過嗎？"

    n "你不知道。"
    n "但你知道，這封信不能就這樣留在箱子裡。"

    menu:
        "你決定怎麼做？":
            "沿著地圖去查個明白":
                jump post_office
            "先把信收好，等之後再說":
                jump delay_bad_end


label post_office:

    scene keelung_post_office
    show filter
    with dissolve

    n "第一站，基隆舊郵局。"

    show m1
    with dissolve

    n "你站在櫃檯前，手裡捏著那封信，心裡卻像被什麼輕輕推著。"
    p "不好意思……我想查一封很久以前的信。"

    show officer
    with dissolve

    n "職員抬頭看了你一眼，沒有多問，只是拿出一張表格，要你先核對信上的資訊。"
    n "紙張摩擦桌面的聲音，讓整個空間顯得格外安靜。"

    show q1
    with dissolve

    n "你仔細看著投遞清單。那些數字排列得像藏著某種規律。"
    n "你開始意識到，這不只是單純的地址，而是祖父留下的第一把鑰匙。"

    # ── 謎題1 ──
    $ user_input = ""
    $ _answered = False
    while not _answered:
        $ user_input = renpy.input("請輸入答案（提示：觀察數字位置）：", length=20).strip()
        if bridge.check_answer(0, user_input):
            $ _answered = True
            $ bridge.save_result(0, 120, 0)
        else:
            n "答案不對，再試試看。"

    n "你終於拼出答案：[user_input]。"
    n "職員看了結果，淡淡地說，這是舊報社的郵遞區號。"
    n "如今那裡早已不是報社，而是文化中心。"

    scene old_post_office
    hide m1
    hide officer
    hide keelung_post_office
    hide filter
    hide q1
    with dissolve

    l "第一次收到這封信，是從舊家的信件堆中撿到的。"
    l "那時候我原本只是想把雜亂的信件整理一下，沒想到，竟會在一疊舊紙裡看見它。"
    l "信封沒有署名，字跡也不算張揚，卻像是從很遠的地方，安靜地落在我手裡。"

    l "我去到郵局想退還，但信封沒署名，郵局職員讓我自己處置那封信。"
    l "那時候我站在櫃檯前，手裡捏著信，心裡卻像是被什麼輕輕碰了一下。"
    l "原本只是想把它還回去，卻沒想到，最後竟是我自己捨不得放下。"

    l "打開信後，那真摯筆跡令我所觸動，我便開始尋找寄件人，希望發現些什麼。"
    l "那字寫得很慢，卻很真。每一筆都像是經過想過、忍過，最後才寫下來。"
    l "我讀著讀著，竟一時忘了時間，只覺得若不去找出寫信的人，心裡總會留著一個缺口。"

    scene keelung_post_office
    show m1
    hide old_post_office
    with dissolve

    n "你低頭看著信。"
    n "這不是一封普通的信。"
    n "這段故事的起點。"

    scene black
    with fade

    jump newspaper_site


label newspaper_site:

    scene bookshelfs
    show filter
    with dissolve

    n "第二站，報社舊址。"
    n "舊建築已經不在，取而代之的是文化中心。"
    n "展覽廳裡有昏黃的燈光，舊報紙與老照片靜靜陳列，像是在替某個年代守夜。"

    show m1
    with dissolve

    n "你在一排書架前停下。"

    show q2
    with dissolve

    n "有些書號排序錯亂，像是有人故意把真正的答案藏了起來。"
    p "祖父……你到底在找誰？"

    # ── 謎題2 ──
    $ user_input = ""
    $ _answered = False
    while not _answered:
        $ user_input = renpy.input("請輸入答案（提示：觀察紅書和粉書）：", length=20).strip()
        if bridge.check_answer(1, user_input):
            $ _answered = True
            $ bridge.save_result(1, 120, 0)
        else:
            n "答案不對，再試試看。"

    n "你翻看資料，發現那段年代的基隆港十分繁盛，船隻往來不歇。"
    n "而在港口時代裡，最重要的東西之一，就是燈塔（[user_input]）。"
    n "港邊的人靠它辨識方向，也靠它等一個可能永遠不會回來的人。"

    scene old_beach
    hide m1
    hide bookshelfs
    hide q2
    with dissolve

    l "我循著信上的內容找到港邊。"
    l "那天的風很大，海浪拍岸的聲音蓋過了腳步聲，也蓋過了我心裡原本的遲疑。"
    l "我原只是想確認一個名字，一個地址，卻沒想到，會在那裡遇見那個站在船旁等人的身影。"

    l "對方站得很安靜，像是早已習慣把等待藏進日常裡。"
    l "我只看了一眼，便記住了那雙在海風裡仍然沒有移開的眼睛。"
    l "那一刻，我忽然明白，這封信真正牽引我的，不只是字句，而是某種說不清的緣分。"

    l "後來，我們常在報社門口交換信件、照片，甚至詩句。"
    l "那不是什麼轟轟烈烈的相遇，只是一次次站在同一個地方，遞出自己最珍惜的東西。"
    l "信紙在手裡慢慢變多，話卻反而越來越少，因為有些心意，已經不必說得太明。"

    l "我和那人逐漸建立情感。"
    l "起初，我還會告訴自己，那只是投緣，是談得來，是剛好懂得彼此。"
    l "可等到某一天，我開始在對方沒來時覺得空落，開始在看見對方時心口發熱，我才知道，自己早已走進了更深的地方。"

    l "友情的界線慢慢模糊。"
    l "我沒有急著替這段關係下定義，只是默默記住每一次相見、每一次等待、每一次分別。"
    l "因為在那個年代裡，有些感情本就不容易被說出口，而越是不說，越會在心裡留下很久很久。"

    scene bookshelfs
    show m1
    hide old_beach
    with dissolve

    n "你忽然有種說不出口的預感。"
    n "那封信的主人，似乎曾經在港邊等過某個人。"

    scene black
    with fade

    jump lighthouse


label lighthouse:

    scene keelung_lighthouse
    with dissolve

    n "第三站，基隆燈塔。"

    show m1
    with dissolve

    n "海風很強，吹得人睜不太開眼。"
    n "你把信攤開，壓在欄杆上，紙角卻還是被風掀得微微顫動。"
    n "你只好用手再按住一角，指尖能感覺到紙張被海風吹得發冷。"

    g "你也是來找故事的嗎？"
    p "這裡……跟信有關？"

    n "管理員沒有立刻回答，只是看了看你手裡的信，又看了看被風吹得幾乎要翻頁的內頁。"
    n "他走近一步，替你把信紙壓平，然後伸手指向內頁的一張小紙條。"

    g "你先看這個。別急著讀字，先看它怎麼被藏起來的。"

    show q3
    with dissolve

    n "紙條上寫著奇怪的符號，像摩斯密碼，又像某種只有兩個人知道的暗號。"

    # ── 謎題3 ──
    $ user_input = ""
    $ _answered = False
    while not _answered:
        $ user_input = renpy.input("請輸入答案（提示：F=..-. G=--. R=.-.）：", length=20).strip()
        if bridge.check_answer(2, user_input):
            $ _answered = True
            $ bridge.save_result(2, 120, 0)
        else:
            n "答案不對，再試試看。"

    n "答案是 [user_input]。"

    hide q3
    show map
    with dissolve

    n "你回想起地圖上那個被紅圈標過的位置，像是在說：真正重要的不是看見，而是等待。"
    n "管理員沉默了一會兒，像是知道你終將走到最後一站。"
    g "你祖父年輕時似乎常在這裡等船靠岸。"
    g "而他等待的，不只是船。"

    show old_beacon
    hide m1
    hide keelung_lighthouse
    hide q3
    with dissolve

    l "那人是船醫助理，常常要出航遠行。"
    l "對方總是與船同行，像是命運本來就不肯讓人輕易留住他。"
    l "我也因此常常在想，自己究竟是在等一艘船靠岸，還是在等一個人回頭。"

    l "我曾偷偷站在燈塔邊，等待著對方的船靠岸，也在那裡讀那人的信。"
    l "海風吹得信紙微微顫動，我卻總是讀得很慢，像怕一不小心，就把那份來之不易的字句看完了。"
    l "燈塔的光一圈一圈掃過海面，也像是在替我照見那些說不出口的心事。"

    l "我正決定要告白時，對方說他將啟程赴美。"
    l "那句話來得太突然，像一陣風把我原本準備好的話全都吹散了。"
    l "我站在原地，明明有很多話想說，最後卻只剩下沉默。"
    l "有些時候，人生就是這樣，差一步就能說出口，卻偏偏在那一步之前，被命運先攔了下來。"

    scene black
    with dissolve

    jump battlement


label battlement:

    scene white_cannon_battlement
    with dissolve

    n "第四站，白米甕砲台。"

    show m1
    with dissolve

    n "你沿著石階往上走，越往上，風聲就越安靜，像是整座山都在替你把腳步聲藏起來。"
    n "海面在遠方泛著白光，和天空幾乎連成一片，讓人一時分不清自己到底是站在山上，還是站在海邊。"

    show map
    with dissolve

    n "你停下來喘了口氣，低頭看著手裡那張已經被折得發軟的地圖。"
    n "一路走到這裡，紙邊早已磨損，顏色也因為反覆摺疊而淡了不少。"
    n "可就在陽光斜斜照上去的那一瞬間，地圖表面竟浮出一層幾乎看不見的六角形暗紋。"

    hide map
    show q4
    with dissolve

    n "你怔了一下，立刻把紙張拿近一些，試著從圖案、數字、邊角去找規律。"
    n "這一題比前面都難，不是因為它多複雜，而是因為它藏得太深。"
    n "它像是在考你，會不會在走到最後的時候，還願意停下來慢慢看。"
    n "有些答案不是想出來的，是一點一點看出來的。"

    # ── 謎題4 ──
    $ user_input = ""
    $ _answered = False
    while not _answered:
        $ user_input = renpy.input("請輸入答案（提示：數數、肩並肩）：", length=20).strip()
        if bridge.check_answer(3, user_input):
            $ _answered = True
            $ bridge.save_result(3, 120, 0)
        else:
            n "答案不對，再試試看。"

    n "最後，你得出答案：[user_input]。"
    n "接著又解出座標：25° N, 121° E。"

    n "你站在砲台上，忽然明白這裡是最後的約定地點。"
    n "祖父曾答應要來，卻沒有來。"
    n "信裡的故事，也在這裡停住。"

    n "你慢慢讀出詩句，像是替祖父把那句沒說出口的話念完。"
    n "\"海風吹信筆封涼，燈塔盼人夜未央。一步錯身終不語，殘章無寄夢偏長。\""

    n "這一刻，你終於明白，這不是一場單純的尋寶。"
    n "這是一段被錯過的愛。"

    menu:
        "你要怎麼面對最後的線索？":
            "立刻去查最終地點":
                jump final_route
            "先回家整理資料":
                jump delay_bad_end


label final_route:

    scene desk_night
    with dissolve

    n "你回到家，翻查舊報、地圖與舊照片。"

    # ── 謎題5 ──
    $ user_input = ""
    $ _answered = False
    while not _answered:
        $ user_input = renpy.input("請輸入答案（提示：顏色重組拼單字）：", length=20).strip()
        if bridge.check_answer(4, user_input):
            $ _answered = True
            $ bridge.save_result(4, 120, 0)
        else:
            n "答案不對，再試試看。"

    n "終於，你發現那個最終線索不是普通店名，而是藏在記憶中的一個字：[user_input]。"
    n "你查到那人後來定居基隆，而他的後代，至今仍住在這片土地上。"
    n "你握緊信紙，知道自己還有最後一次機會。"

    scene taiping_qingniao_bookstore
    with dissolve

    n "最終站，太平青鳥書店。"
    n "你推開門時，鈴鐺聲清脆地響了一下。"
    n "書香混著木頭與咖啡的味道，讓人不自覺放慢呼吸。"

    o "……你找誰？"
    p "我想找一位，和我祖父在很久以前認識的人。"

    n "你遞出那封信，也遞出那張舊照片。"
    n "男子起初還有些疑惑，直到他看見照片背面的字跡。"
    n "他的眼神，慢慢變了。"

    s "……這張照片，我家裡也有一張。"

    n "他安靜很久，最後低頭輕輕笑了。"
    n "那笑容裡沒有驚訝，只有某種終於被接上的理解。"

    s "原來……他一直沒有忘記。"

    n "你把信交給他。"
    n "這一次，沒有再錯過。"

    # 顯示最終分數
    $ total = bridge.get_total_score()
    n "你完成了所有謎題，總分：[total] 分。"

    jump good_end


label good_end:

    scene sunset_sea
    with dissolve

    n "好結局。"
    n "祖父沒有說完的話，終於被傳到了該去的人手上。"
    n "你站在海邊，看著夕陽把整片天空染成溫柔的橘紅色，第一次覺得，錯過不是結束，傳達才是。"

    return


label delay_bad_end:

    scene empty_station
    with dissolve

    n "你猶豫了。"
    n "你告訴自己，等一下再去也沒關係。"
    n "可是有些事，一旦晚了，就不會再等人。"

    n "當你終於再回到線索所在的地方時，門已經關了。"
    n "人不在，照片不在，唯一留下的只有風。"

    n "你手裡還握著那封信，卻再也找不到能親手接住它的人。"

    n "壞結局。"
    n "你解開了謎題，卻錯過了真正重要的相遇。"

    return
