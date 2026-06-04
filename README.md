# 未曾寄出的思念，由你傳達

一款以基隆為背景的點擊解謎視覺小說。

---

## 系統需求

- Ubuntu 24.04
- gcc
- make
- Ren'Py 8.5.3（Linux 版）

---

## 安裝步驟

### 1. 安裝必要套件
```bash
sudo apt update
sudo apt install gcc make bzip2 wget
```

### 2. 下載並解壓縮 Ren'Py
```bash
wget https://www.renpy.org/dl/8.5.3/renpy-8.5.3-sdk.tar.bz2
tar -xjf renpy-8.5.3-sdk.tar.bz2
```

### 3. 下載專案
```bash
git clone https://github.com/fionaliu0621/Programming-II-Project.git
```

### 4. 編譯 C 核心
```bash
cd Programming-II-Project/core
make
cd ../..
```

確認 `core/` 資料夾內出現 `libtcth_core.so`。

---

## 執行遊戲
```bash
cd renpy-8.5.3-sdk
./renpy.sh ../Programming-II-Project
```
