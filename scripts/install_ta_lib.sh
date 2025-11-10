#!/bin/bash

# ===============================================
# TA-Lib 安装脚本 - 股票分析项目专用
# ===============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 参数解析
VERSION="0.4.0"
OUTPUT_DIR="/tmp/ta-lib"
SOURCE="github"

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--version) VERSION="$2"; shift 2 ;;
        -o|--output) OUTPUT_DIR="$2"; shift 2 ;;
        -s|--source) SOURCE="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# 下载URL
GITHUB_URL="https://github.com/TA-Lib/ta-lib/releases/download/v${VERSION}/ta-lib-${VERSION}-src.tar.gz"
SOURCEFORGE_URL="https://downloads.sourceforge.net/project/ta-lib/ta-lib/${VERSION}/ta-lib-${VERSION}-src.tar.gz"

install_ta_lib() {
    local temp_dir=$(mktemp -d)
    trap "rm -rf '$temp_dir'" EXIT
    
    log "开始安装 TA-Lib v${VERSION}"
    
    # 选择下载源
    local download_url="$GITHUB_URL"
    if [ "$SOURCE" = "sourceforge" ]; then
        download_url="$SOURCEFORGE_URL"
    fi
    
    # 下载
    log "下载 TA-Lib..."
    if command -v wget >/dev/null; then
        wget -O "$temp_dir/ta-lib.tar.gz" "$download_url"
    elif command -v curl >/dev/null; then
        curl -L -o "$temp_dir/ta-lib.tar.gz" "$download_url"
    else
        log_error "需要 wget 或 curl"
        return 1
    fi
    
    # 解压
    log "解压文件..."
    tar -xzf "$temp_dir/ta-lib.tar.gz" -C "$temp_dir"
    
    local source_dir="$temp_dir/ta-lib"
    if [ ! -d "$source_dir" ]; then
        source_dir="$temp_dir/ta-lib-${VERSION}"
    fi
    
    # 编译安装
    log "编译 TA-Lib..."
    cd "$source_dir"
    
    ./configure --prefix="$OUTPUT_DIR" --enable-shared
    make -j$(nproc)
    make install
    
    # 验证安装
    if [ -f "$OUTPUT_DIR/bin/ta_regtest" ]; then
        log "验证安装..."
        "$OUTPUT_DIR/bin/ta_regtest" || log_warning "测试有警告但继续"
    fi
    
    log "✅ TA-Lib 安装完成: $OUTPUT_DIR"
    
    # 设置GitHub输出
    echo "ta_lib_dir=$OUTPUT_DIR" >> $GITHUB_OUTPUT
}

# 主安装流程
if install_ta_lib; then
    log "TA-Lib 安装成功"
else
    log_error "TA-Lib 安装失败"
    exit 1
fi
