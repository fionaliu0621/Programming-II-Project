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
define l = Character("林正雄", color="#000000")
define c = Character("郵務員", color="#1f2b50")
define g = Character("管理員", color="#1f2b50")
define s = Character("王子騫", color="#1f2b50")
define k = Character("店員", color="#1f2b50")
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

image guard:
    "images/guard.png"
    zoom 0.9
    xanchor 0.9
    yanchor 0.9
    xpos 650
    ypos 1000

image waiter:
    "images/waiter.png"
    zoom 0.8
    xanchor 0.8
    yanchor 0.8
    xpos 650
    ypos 1000

image grandson:
    "images/grandson.png"
    zoom 0.77
    xanchor 0.77
    yanchor 0.77
    xpos 650
    ypos 1000

image map:
    "images/map.png"
    xpos 1050

image old_photo:
    "images/old_photo.png"
    zoom 0.55
    xanchor 0.55
    yanchor 0.55
    xpos 1010
    ypos 400

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
    
image q5:
    "images/q5.png"
    zoom 0.55
    xanchor 0.55
    yanchor 0.55
    xpos 1010
    ypos 400

default puzzle_score = 0
default final_keyword = ""

# ── 規則說明 ───────────────────────────────────────────────────────
label start:

    scene rule
    with dissolve

    n "遊玩前提醒"
    n "1. 建議在重要決策前先行存檔，以免錯過關鍵劇情分支。"
    n "2. 本作所有謎題皆有固定作答格式，請仔細閱讀題目說明。"
    n "3. 部分線索可能藏在對話、場景與圖片細節中，請留意畫面資訊。"
    n "4. 若忘記先前出現的提示，可使用快速選單中的「歷史」回顧內容。"
    n "5. 本作包含多個分支與結局，玩家的選擇將影響故事的最終走向。"
    n "遊戲即將開始，祝您有個美好的體驗！"

    jump old_house_room

# ── 遊戲開始 ───────────────────────────────────────────────────────
label old_house_room:

    scene black
    with fade
    play music "audio/now.mp3" fadein 1.0

    n "祖父林正雄過世後的第三天，你回到久未整理的老家。"
    n "房間裡還留著舊木櫃的氣味，午後的光從半掩的窗簾縫隙斜斜落下，照亮空氣裡漂浮的灰塵。"

    scene old_house_room
    with dissolve
    show m1

    n "你原本只是想把遺物分門別類，卻在最角落的櫃子裡，拖出了一只泛黃的舊皮箱。"
    n "皮箱的皮面已經裂開，金屬扣環微微生鏽，像是很久很久以前，就沒有人再碰過它。"

    p "……這是什麼？"

    play sound "audio/zipper.ogg" 

    hide m1
    show envolope:
        ypos -150
    with dissolve

    n "你打開皮箱。裡面沒有值錢的東西，只有幾張舊照片、一疊泛黃紙張，和一封沒有寄出的信。"
    n "信封上只寫著名字：林正雄。"
    n "筆跡很工整，卻像是被什麼壓抑著，連收信人都沒有寫完。"

    hide envolope
    show envolope1
    play sound "audio/envelope.ogg"
    with dissolve

    n "你抽出信紙，紙張薄得像會在手中碎掉。"
    n "那是一封寫於 1960 年的信。"
    n "而信的背面，還藏著一張手繪的基隆地圖。"

    hide envolope1
    show map:
        xpos 100
    play sound "audio/envelope.ogg"
    with dissolve

    n "地圖上標了四個地點。"
    n "舊郵局、報社舊址、燈塔、白米甕砲台。"
    n "每一個點旁邊都畫了小小的記號，像是某段回憶被刻意留下的路標。"

    show m1
    with dissolve
    play sound "audio/envelope.ogg"
    p "這些地方……祖父去過嗎？"

    n "你不知道。"
    n "但你知道，這封信不能就這樣留在箱子裡。"

    menu:
        "你決定怎麼做？"
        "沿著地圖去查個明白":
            jump post_office
        "先把信收好，等之後再說":
            jump ending_box

# ── 場景一 郵局 ───────────────────────────────────────────────────────
label post_office:
    scene black
    with fade
    scene keelung_post_office
    show filter
    with dissolve

    n "第一站，基隆舊郵局。"

    show m1
    with dissolve

    n "你抽了號碼牌，在櫃檯前等著。冷白色的燈光照在地磚上，讓整個空間顯得格外安靜。"
    n "你手裡捏著那封信，心裡卻像被什麼輕輕推著。"
    p "不好意思……我想查一封很久以前的信。"

    show officer
    with dissolve

    c "沒有完整資訊很難查，你先對一下這些資料。"
    n "對方把一張投遞清單推到你面前。上面是一串數字與分數般的標記，看上去像題目，也像祖父刻意留下的第一道門。"

    show q1
    play sound "audio/paper.ogg"
    with dissolve

    n "你仔細看著投遞清單。那些數字排列得像藏著某種規律。"
    n "你開始意識到，這不只是單純的地址，而是祖父留下的第一把鑰匙。"

    # ── 謎題1 ──
    $ bridge.start_timer(0)
    $ _hint_index = 0
    $ _show_hint_prompt = False
    $ user_input = ""
    $ _answered = False
    while not _answered:
        $ _elapsed = bridge.get_elapsed(0)
        if _elapsed >= 60 and not _show_hint_prompt and _hint_index <= 2:
            $ _show_hint_prompt = True
            menu:
                "已經一分鐘了，需要提示嗎？"
                "給我提示":
                    $ _hint = bridge.get_hint(0, 999, _hint_index)
                    if _hint:
                        n "[_hint]"
                        $ _hint_index = _hint_index + 1
                    else:
                        n "目前還沒有更多提示了。"
                "我再想想":
                    pass
        $ user_input = renpy.input("請輸入5位數答案（提示：觀察數字位置）：", length=20).strip()
        if bridge.check_answer(0, user_input):
            $ _answered = True
            $ bridge.save_result(0, 0)
        else:
            play sound "audio/wrong.ogg"
            menu:
                "答案不對！需要提示嗎？"
                "給我提示":
                    $ _hint = bridge.get_hint(0, 999, _hint_index)
                    if _hint and _hint_index <= 2:
                        n "[_hint]"
                        $ _hint_index = _hint_index + 1
                    else:
                        n "目前還沒有更多提示了。"
                "我再想想":
                    $ _show_hint_prompt = False
    
    play sound "audio/success.ogg"
            
    n "最後，你解出了[user_input]。那是基隆舊報社的郵遞區號，而那個地方如今正是文化中心。"
    c "以前有些沒有署名的信，最後也只能由撿到的人決定去留。"
    n "那句話讓你短暫愣住。祖父第一次拿到那封信，正是因為它混在舊家的信堆裡，後來帶來郵局退還，卻被告知自行處置。"

    $ theBox = "gui/memo_textbox.png"
    scene old_post_office
    play music "audio/past.mp3" fadein 1.0
    $ textbox_mode = "gray"
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

    $ theBox = "gui/textbox.png"
    scene keelung_post_office
    play music "audio/now.mp3" fadein 1.0
    show m1
    hide old_post_office
    with dissolve

    n "你低頭看著信。"
    n "這不是一封普通的信。"
    n "這段故事的起點。"

    scene black
    with fade

    jump newspaper_site

# ── 場景二 報社 ───────────────────────────────────────────────────────
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
    play sound "audio/paper.ogg"
    with dissolve

    n "你抽出幾本紅色與粉色書脊的書，紙頁有霉味，像把舊時代的空氣重新翻了出來。"
    p "祖父……你到底在找誰？"

    # ── 謎題2 ──
    $ bridge.start_timer(1)
    $ _hint_index = 0
    $ _show_hint_prompt = False
    $ user_input = ""
    $ _answered = False
    while not _answered:
        $ _elapsed = bridge.get_elapsed(1)
        if _elapsed >= 60 and not _show_hint_prompt and _hint_index <= 2:
            $ _show_hint_prompt = True
            menu:
                "已經一分鐘了，需要提示嗎？"
                "給我提示":
                    $ _hint = bridge.get_hint(1, 999, _hint_index)
                    if _hint:
                        n "[_hint]"
                        $ _hint_index = _hint_index + 1
                    else:
                        n "目前還沒有更多提示了。"
                "我再想想":
                    pass
        $ user_input = renpy.input("請輸入答案（照1~6之順序拼出單字）：", length=20).strip()
        if bridge.check_answer(1, user_input):
            $ _answered = True
            $ bridge.save_result(1, 0)
        else:
            play sound "audio/wrong.ogg"
            menu:
                "答案不對！需要提示嗎？"
                "給我提示":
                    $ _hint = bridge.get_hint(1, 999, _hint_index)
                    if _hint and _hint_index <= 2:
                        n "[_hint]"
                        $ _hint_index = _hint_index + 1
                    else:
                        n "目前還沒有更多提示了。"
                "我再想想":
                    $ _show_hint_prompt = False
    
    play sound "audio/success.ogg"
             
    n "你翻看資料，發現那段年代的基隆港十分繁盛，船隻往來不歇。"
    n "而在港口時代裡，最重要的東西之一，就是燈塔（[user_input]）。"
    n "港邊的人靠它辨識方向，也靠它等一個可能永遠不會回來的人。"

    $ theBox = "gui/memo_textbox.png"
    scene old_beach
    play music "audio/past.mp3" fadein 1.0
    hide filter
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

    $ theBox = "gui/textbox.png"
    scene bookshelfs
    play music "audio/now.mp3" fadein 1.0
    show filter
    show m1
    hide old_beach
    with dissolve

    n "你忽然有種說不出口的預感。"
    n "那封信的主人，似乎曾經在港邊等過某個人。"

    scene black
    with fade

    jump lighthouse

# ── 場景三 燈塔 ───────────────────────────────────────────────────────
label lighthouse:

    scene keelung_lighthouse
    show filter
    with dissolve

    n "第三站，基隆燈塔。"

    show m1
    with dissolve

    n "海風很強，吹得人睜不太開眼。"
    n "你把信攤開，壓在欄杆上，紙角卻還是被風掀得微微顫動。"
    n "你只好用手再按住一角，指尖能感覺到紙張被海風吹得發冷。"

    show guard
    with dissolve

    g "你也是來找故事的嗎？"
    p "這裡……跟信有關？"

    n "管理員沒有立刻回答，只是看了看你手裡地信，又看了看被風吹得幾乎要翻頁的內頁。"
    n "他走近一步，替你把信紙壓平，然後伸手指向內頁的一張小紙條。"

    g "你先看這個。別急著讀字，先看它怎麼被藏起來的。"

    show q3
    with dissolve

    n "紙條上寫著奇怪的符號，像摩斯密碼，又像某種只有兩個人知道的暗號。"
    n "符號旁邊還有幾個被刻意畫下的記號，彷彿在提醒你，真正的答案不只在字裡，也在它被放進信裡的方式。"

    # ── 謎題3 ──
    $ bridge.start_timer(2)
    $ _hint_index = 0
    $ _show_hint_prompt = False
    $ user_input = ""
    $ _answered = False
    while not _answered:
        $ _elapsed = bridge.get_elapsed(2)
        if _elapsed >= 60 and not _show_hint_prompt and _hint_index <= 2:
            $ _show_hint_prompt = True
            menu:
                "已經一分鐘了，需要提示嗎？"
                "給我提示":
                    $ _hint = bridge.get_hint(2, 999, _hint_index)
                    if _hint:
                        n "[_hint]"
                        $ _hint_index = _hint_index + 1
                    else:
                        n "目前還沒有更多提示了。"
                "我再想想":
                    pass
        $ user_input = renpy.input("請輸入答案（請用大寫回答本題）：", length=20).strip()
        if bridge.check_answer(2, user_input):
            $ _answered = True
            $ bridge.save_result(2, 0)
        else:
            play sound "audio/wrong.ogg"
            menu:
                "答案不對！需要提示嗎？"
                "給我提示":
                    $ _hint = bridge.get_hint(2, 999, _hint_index)
                    if _hint and _hint_index <= 2:
                        n "[_hint]"
                        $ _hint_index = _hint_index + 1
                    else:
                        n "目前還沒有更多提示了。"
                "我再想想":
                    $ _show_hint_prompt = False 
            
    play sound "audio/success.ogg"
            
    n "答案是 白 [user_input]。"

    hide q3
    play sound "audio/paper.ogg"
    show map
    with dissolve

    n "你回想起地圖上那個被紅圈標過的位置，像是在說：真正重要的不是看見，而是等待。"
    n "管理員沉默了一會兒，像是知道你終將走到最後一站。"
    g "你祖父年輕時似乎常在這裡等船靠岸。"
    g "而他等待的，不只是船。"

    $ theBox = "gui/memo_textbox.png"
    show old_beacon
    play music "audio/past.mp3" fadein 1.0
    hide filter
    hide m1
    hide keelung_lighthouse
    hide q3
    hide guard
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

    $ theBox = "gui/textbox.png"
    scene black
    with dissolve

    jump battlement

# ── 場景四 白米甕 ───────────────────────────────────────────────────────
label battlement:

    scene white_cannon_battlement
    play music "audio/now.mp3" fadein 1.0
    show filter
    with dissolve

    n "第四站，白米甕砲台。"

    show m1
    with dissolve

    n "你沿著石階往上走，越往上，風聲就越安靜，像是整座山都在替你把腳步聲藏起來。"
    n "海面在遠方泛著白光，和天空幾乎連成一片，讓人一時分不清自己到底是站在山上，還是站在海邊。"

    show map
    play sound "audio/paper.ogg"
    with dissolve

    n "你停下來喘了口氣，低頭看著手裡那張已經被折得發軟的地圖。"
    n "一路走到這裡，紙邊早已磨損，顏色也因為反覆摺疊而淡了不少。"
    n "可就在陽光斜斜照上去的那一瞬間，地圖表面竟浮出一層幾乎看不見的六角形暗紋。"

    hide map
    show q4
    play sound "audio/paper.ogg"
    with dissolve

    n "你怔了一下，立刻把紙張拿近一些，試著從圖案、數字、邊角去找規律。"
    n "這一題比前面都難，不是因為它多複雜，而是因為它藏得太深。"
    n "它像是在考你，會不會在走到最後的時候，還願意停下來慢慢看。"
    n "有些答案不是想出來的，是一點一點看出來的。"

    # ── 謎題4 ──
    $ bridge.start_timer(3)
    $ _hint_index = 0
    $ _show_hint_prompt = False
    $ user_input = ""
    $ _answered = False
    while not _answered:
        $ _elapsed = bridge.get_elapsed(3)
        if _elapsed >= 60 and not _show_hint_prompt and _hint_index <= 2:
            $ _show_hint_prompt = True
            menu:
                "已經一分鐘了，需要提示嗎？"
                "給我提示":
                    $ _hint = bridge.get_hint(3, 999, _hint_index)
                    if _hint:
                        n "[_hint]"
                        $ _hint_index = _hint_index + 1
                    else:
                        n "目前還沒有更多提示了。"
                "我再想想":
                    pass
        $ user_input = renpy.input("請輸入答案（答案格式為__, ___）：", length=20).strip()
        if (bridge.check_answer(3, user_input) or bridge.check_answer(3, user_input.replace(" ", "").replace("，", ",").replace(",", ","))):
            $ _answered = True
            $ bridge.save_result(3, 0)
        else:
            play sound "audio/wrong.ogg"
            menu:
                "答案不對！需要提示嗎？"
                "給我提示":
                    $ _hint = bridge.get_hint(3, 999, _hint_index)
                    if _hint and _hint_index <= 2:
                        n "[_hint]"
                        $ _hint_index = _hint_index + 1
                    else:
                        n "目前還沒有更多提示了。"
                "我再想想":
                    $ _show_hint_prompt = False
            
    play sound "audio/success.ogg"
            
    n "最後，你得出答案：[user_input]。"
    n "接著又解出座標：25° N, 121° E。"

    hide q4
    with dissolve

    n "你站在砲台上，忽然明白這裡是最後的約定地點。"
    n "祖父曾答應要來，卻沒有來。"
    n "信裡的故事，也在這裡停住。"

    $ theBox = "gui/memo_textbox.png"
    show old_cannon
    play music "audio/past.mp3" fadein 1.0
    hide filter
    hide m1
    hide white_cannon_battlement
    hide q4
    with dissolve

    l "我們最後一次見面時，他對我說：『我在砲台等你。』"
    l "那句話我一直記得很清楚，甚至直到很多年後，回想起來仍像是當時才剛說完。"
    l "我明明答應了他的邀約，心裡也不是沒有想過要去。"

    l "可到了最後，我還是沒有去。"
    l "有些害怕說不清，也有些害怕一旦真的見了面，自己便再也無法假裝只是普通朋友。"
    l "我就那樣站在原地，讓那份本該說出口的心意，停在還沒開始的地方。"

    l "那封信，也就此塵封在皮箱。"
    l "它沒有寄出去，也沒有被我再拿出來看過。"
    l "像是我替自己留下的一個沉默的證明，提醒我有些話，一旦錯過了時機，就只能跟著歲月一起封存。"

    $ theBox = "gui/textbox.png"
    hide old_cannon
    show white_cannon_battlement
    play music "audio/now.mp3" fadein 1.0
    show filter
    show m1
    with dissolve
    
    n "你的腦海裡慢慢浮出一篇詩，是祖父在你小時候教會你的，但你當時不知道這篇詩是什麼意思。"
    n "你慢慢讀出詩句，像是替祖父把那句沒說出口的話念完。"
    n "海風吹信筆封涼，燈塔盼人夜未央。一步錯身終不語，殘章無寄夢偏長。"

    n "這一刻，你終於明白，這不是一場單純的尋寶。"
    n "這是一段被錯過的愛。"

    menu:
        "你要怎麼面對最後的線索？"
        "立刻去查最終地點":
            scene black
            with dissolve
            jump final_route
        "先回家整理資料":
            scene black
            with dissolve
            jump delay_bad_end


label final_route:

    scene old_house_room
    show m1
    with dissolve

    n "你回家後翻查舊報，果然找到關於颱風的紀錄：祖父沒赴約的那一天，對方的船其實也因風雨沒有啟航。那不是永別，而是另一種更漫長的錯過。"
    n "你大喜過望，繼續追查，發現那人後來定居基隆，甚至留下了後代。"
    n "就在你以為線索快要斷掉時，你在舊照片與報紙之間，發現了一張被壓在最底下的紙條。"

    show q5
    play sound "audio/paper.ogg"
    with dissolve

    # ── 謎題5 ──
    $ bridge.start_timer(4)
    $ _hint_index = 0
    $ _show_hint_prompt = False
    $ user_input = ""
    $ _answered = False
    while not _answered:
        $ _elapsed = bridge.get_elapsed(4)
        if _elapsed >= 60 and not _show_hint_prompt and _hint_index <= 2:
            $ _show_hint_prompt = True
            menu:
                "已經一分鐘了，需要提示嗎？"
                "給我提示":
                    $ _hint = bridge.get_hint(4, 999, _hint_index)
                    if _hint:
                        n "[_hint]"
                        $ _hint_index = _hint_index + 1
                    else:
                        n "目前還沒有更多提示了。"
                "我再想想":
                    pass
        $ user_input = renpy.input("請輸入答案（請用大寫回答本題）：", length=20).strip()
        if bridge.check_answer(4, user_input):
            $ _answered = True
            $ bridge.save_result(4, 0)
        else:
            play sound "audio/wrong.ogg"
            menu:
                "答案不對！需要提示嗎？"
                "給我提示":
                    $ _hint = bridge.get_hint(4, 999, _hint_index)
                    if _hint and _hint_index <= 2:
                        n "[_hint]"
                        $ _hint_index = _hint_index + 1
                    else:
                        n "目前還沒有更多提示了。"
                "我再想想":
                    $ _show_hint_prompt = False
            
    play sound "audio/success.ogg"
            
    n "終於，你發現那個最終線索不是普通店名，而是藏在記憶中的一個字：[user_input]。"
    n "你查到那人後來定居基隆，而他的後代，至今仍住在這片土地上。"
    n "你握緊信紙，知道自己還有最後一次機會。"

    # 顯示最終分數
    $ total = bridge.get_total_score()
    n "你完成了所有謎題，總分：[total] 分。"

    menu:
        "解出此題後，請問你如何理解 CAFE？"
        "是港邊老咖啡館，去海港附近找":
            $ final_keyword = "harbor"
        "是書店裡的咖啡角落，去太平青鳥書店":
            $ final_keyword = "bookstore"
        "是祖父以前常去的茶室，回老街找":
            $ final_keyword = "teahouse"

    if final_keyword == "bookstore":
        jump final_bookstore
    elif final_keyword == "harbor":
        jump final_harbor
    else:
        jump final_teahouse

# ── 擴充結局 ───────────────────────────────────────────────────────
label final_bookstore:

    scene taiping_qingniao_bookstore
    show filter
    with dissolve

    n "最終站，太平青鳥書店。"
    play sound "audio/door.ogg"
            
    show m1
    with dissolve

    n "你推開門時，鈴鐺聲清脆地響了一下。"
    n "書香混著木頭與咖啡的味道，讓人不自覺放慢呼吸。"

    show waiter
    with dissolve

    o "……你找誰？"
    p "我想找一位，和我祖父在很久以前認識的人。"

    n "你把信和那張舊照片一併遞了過去。"
    n "剛好店裡只有一位顧客，服務生把照片傳給那位客人看。"

    hide waiter

    if total == 20:
        jump ending_true_good
    else:
        jump ending_soft_good

label ending_true_good:
    play music "audio/good.mp3" fadein 1.0
    scene taiping_qingniao_bookstore
    show filter
    show m1
    show grandson
    with dissolve
    
    n "男子原本只是禮貌地接下，目光卻在碰到照片的一瞬間停住了。"
    n "他沒有立刻說話，只是低頭看著那張照片，像是在辨認某個早就被時間磨淡的輪廓。"

    n "過了好一會兒，他才伸手翻到背面。"
    n "當他看見那熟悉的字跡時，神情微微一震。"
    n "那不是驚訝得很劇烈的反應，而是一種被記憶輕輕碰到之後，慢慢浮上來的沉默。"

    s "……這張照片，我家裡也有一張。"

    n "他安靜了很久，像是在把心裡某個模糊的地方，重新對上眼前的影子。"
    n "最後，他低頭輕輕笑了。"
    n "那笑容裡沒有驚訝，只有某種終於被接上的理解。"

    s "原來……他一直沒有忘記。"
    n "那一刻，你忽然覺得，祖父藏了一生、沒能親手送出的心意，終於在你手上，真正抵達了該去的地方。"

    n "男子從包裡拿出筆記本翻找，過了一會兒，遞出一張已經有些泛黃的舊照片。"

    show old_photo
    with dissolve
    
    n "照片裡的兩個人，站在港邊，隔著歲月仍能看見年輕時不敢說破的情意。"
    n "你知道，這不只是你替祖父完成了一次傳達，也是兩段被時間分開的記憶，終於在今日重新接上。"

    scene sunset_sea
    hide taiping_qingniao_bookstore
    hide grandson
    show m1
    with dissolve

    n "離開書店時，天色正好。山城的風從街口慢慢吹下來，帶著一點海的氣味。"
    n "你回頭望向遠處的港口，忽然明白，有些故事不是為了被改寫，而是為了在多年以後，仍能被好好理解。"
    n "而那些未曾寄出的思念，也終於有人替它走完最後一程。"
    n "真結局【由你傳達】。"

    return

label ending_soft_good:
    play music "audio/good.mp3" fadein 1.0
    scene taiping_qingniao_bookstore
    show filter
    show m1
    show grandson
    with dissolve

    n "你還是把信送到了正確的人手上。"
    n "男子接過信時，神情有些恍惚，像是聽見了一段自己從未真正知道、卻又隱約熟悉的往事。"

    n "他沒有立刻把話說得很滿，只是將信小心收好，低聲說自己會回去把家裡那張舊照片找出來。"
    n "你知道，雖然你沒有拼齊所有細節，沒能把祖父和那人之間的每一段經過都完整說清，但至少這封信，終究沒有再被埋進沉默裡。"

    scene sunset_sea
    hide taiping_qingniao_bookstore
    hide grandson
    show m1
    with dissolve

    n "走出書店時，天色已經有些暗了。玻璃門映著街燈，也映著你手裡空下來的位置。"
    n "你忽然覺得，也許有些故事不必知道全部，才能被溫柔地保存。"
    n "只要它終究被送到了願意接住的人手裡，那份遲來的回音，就已經足夠。"
    n "好結局【遲來的回音】。"

    return

label final_harbor:
    scene old_harbor_cafe
    with dissolve
    n "你去了港邊一間老咖啡館。窗邊能看見船影，桌椅老舊，牆上掛著泛黃船照。這裡很像故事會停留的地方，卻沒有任何人認得你手上的名字。"
    n "店主聽完後只說，這附近以前的確有很多等船的人，但太久了，太多人都散了。"
    n "臨走前，店主忽然想起有人也許知道更多，提到山上的書店曾收過不少地方口述資料。你意識到自己差一點走錯方向。"
    menu:
        "要不要立刻改去書店？"
        "去，還來得及":
            jump final_bookstore
        "不了，今天就到這裡":
            jump ending_missed

label final_teahouse:
    scene old_street_teahouse
    show m1
    with dissolve
    n "你回到老街尋找祖父可能去過的茶室。"
    n "舊街潮濕、招牌斑駁，午後的光照不進狹窄騎樓。"
    n "你找到一間還在營業的老店，卻只在角落裡看見與祖父相似的時代殘影。"
    n "你把信攤在桌上，看著茶湯表面慢慢晃動，忽然明白自己追到的只是祖父熟悉的地方，不是那封信真正要去的地方。"
    jump ending_wrong_place

label ending_missed:
    play music "audio/bad.mp3" fadein 1.0
    scene harbor_evening
    show filter
    show m1
    with dissolve
    
    n "你離開港邊時，海風很大，吹得外套下襬不住晃動。"
    n "咖啡館裡沒有你要找的人，窗邊只剩幾張空桌，和幾個被黃昏拉長的影子。"

    n "你本以為自己已經追到最後一步，卻在回頭查證時才知道，那個真正能收下這封信的人，其實一直都在山上的那間書店裡。"
    n "不是線索騙了你，而是你在最後關頭，把答案理解成了另一個更像回憶、卻不是真相的方向。"

    n "你站在港邊，望著遠處逐漸暗下去的海面，忽然想起祖父沒有赴約的那一天。"
    n "原來有些錯過並不轟烈，它只是安安靜靜地發生在你以為『差不多了』的那一刻。"
    n "你不是沒有走到最後，只是在最後一步，和答案錯身而過。"
    n "壞結局【擦身而過】。"

    menu:
        "要重新開始嗎？"
        "重新開始":
            jump old_house_room
        "結束遊戲":
            return


label ending_wrong_place:
    play music "audio/bad.mp3" fadein 1.0
    scene empty_teacup
    show m1
    with dissolve

    n "你到了那間充滿回憶的老茶室。"
    n "斑駁的木桌、溫吞的茶香、牆面泛黃的痕跡，一切都像極了祖父可能停留過的年代。"

    n "你坐了很久，甚至一度以為自己找對了地方。"
    n "可時間一點一點過去，始終沒有人認得信上的名字，也沒有人能把這封信接過去。"
    n "你這才明白，你找到的是一個很像故事會停留的地方，卻不是這封信真正該抵達的地方。"

    n "茶早已放涼，信卻還在你手裡。"
    n "那一刻你忽然懂了，思念並不是只要有個地方安放就夠了。"
    n "它真正想去的，是某一個人，是某一雙願意看完它、理解它、接住它的手。"
    n "而你終究沒能替祖父，把信送到正確的地址。"
    n "壞結局【寄不到的地址】。"

    menu:
        "要重新開始嗎？"
        "重新開始":
            jump old_house_room
        "結束遊戲":
            return

label delay_bad_end:
    play music "audio/bad.mp3" fadein 1.0
    scene empty_station
    with dissolve

    n "你已經知道祖父曾錯過一場重要的赴約，也知道那封信為什麼沒有寄出。"
    n "白米甕砲台上的風、燈塔邊的等待、港邊沒能說出口的情意，到了這裡，似乎已經足夠拼湊成一個完整的遺憾。"

    n "你猶豫了。"
    n "你告訴自己，等一下再去也沒關係。"
    n "可是有些事，一旦晚了，就不會再等人。"

    n "當你終於再回到線索所在的地方時，店已經停業了。"
    n "人不在，照片不在，唯一留下的只有風。"

    n "你手裡還握著那封信，卻再也找不到能親手接住它的人。"

    n "你解開了謎題，卻錯過了真正重要的相遇。"
    n "壞結局【來不及】"

    menu:
        "要重新開始嗎？"
        "重新開始":
            jump old_house_room
        "結束遊戲":
            return

label ending_box:
    scene black
    with fade

    play music "audio/bad.mp3" fadein 1.0
    scene old_house_room
    with dissolve

    n "你把皮箱重新扣上，金屬扣環發出一聲很輕的聲響，像是某段故事又一次被關回了時間裡。"
    n "灰塵慢慢落回箱面，房間也重新安靜下來，彷彿你從來沒有打開過它。"

    n "那封寫於 1960 年的信仍然躺在裡面，紙頁泛黃、邊角脆弱，像一段始終沒能說出口的話。"
    n "祖父沒有寄出的心意，到了你這裡，依舊沒有被傳達。"

    n "有些故事會因為被發現而重新活過來。"
    n "可也有些故事，若沒有人願意把它讀完，它就只能繼續沉在箱底，與歲月一同老去。"
    n "早期結局【箱底】。"

    menu:
        "要重新開始嗎？"
        "重新開始":
            jump old_house_room
        "結束遊戲":
            return