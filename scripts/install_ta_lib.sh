#!/bin/bash

# ===============================================
# TA-Lib 安装脚本 - 股票分析项目专用
# GitHub Actions 优化版本
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
    log "安装目录: $OUTPUT_DIR"
    
    # 选择下载源
    local download_url="$GITHUB_URL"
    if [ "$SOURCE" = "sourceforge" ]; then
        download_url="$SOURCEFORGE_URL"
        log "使用 SourceForge 下载源"
    else
        log "使用 GitHub 下载源"
    fi
    
    # 下载
    log "下载 TA-Lib..."
    if command -v wget >/dev/null 2>&1; then
        if ! wget --progress=bar:force -O "$temp_dir/ta-lib.tar.gz" "$download_url"; then
            log_error "wget 下载失败"
            return 1
        fi
    elif command -v curl >/dev/null 2>&1; then
        if ! curl -L --progress-bar -o "$temp_dir/ta-lib.tar.gz" "$download_url"; then
            log_error "curl 下载失败"
            return 1
        fi
    else
        log_error "需要 wget 或 curl"
        return 1
    fi
    
    # 检查文件是否下载成功
    if [ ! -s "$temp_dir/ta-lib.tar.gz" ]; then
        log_error "下载的文件为空或不存在"
        return 1
    fi
    
    log "下载完成，文件大小: $(du -h "$temp_dir/ta-lib.tar.gz" | cut -f1)"
    
    # 解压
    log "解压文件..."
    if ! tar -xzf "$temp_dir/ta-lib.tar.gz" -C "$temp_dir"; then
        log_error "解压失败"
        return 1
    fi
    
    # 查找源代码目录
    local source_dir
    if [ -d "$temp_dir/ta-lib" ]; then
        source_dir="$temp_dir/ta-lib"
    elif [ -d "$temp_dir/ta-lib-${VERSION}" ]; then
        source_dir="$temp_dir/ta-lib-${VERSION}"
    else
        log_error "未找到源代码目录"
        ls -la "$temp_dir/"
        return 1
    fi
    
    log "源代码目录: $source_dir"
    
    # 检查配置脚本
    if [ ! -f "$source_dir/configure" ]; then
        log_error "未找到 configure 脚本"
        return 1
    fi
    
    # 编译安装
    log "编译 TA-Lib..."
    cd "$source_dir"
    
    # 运行配置脚本
    if ! ./configure --prefix="$OUTPUT_DIR" --enable-shared --disable-static; then
        log_error "配置失败"
        return 1
    fi
    
    # 编译
    local cpu_count=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 2)
    log "使用 $cpu_count 个CPU核心进行编译"
    
    if ! make -j$cpu_count; then
        log_error "编译失败"
        return 1
    fi
    
    # 安装
    if ! make install; then
        log_error "安装失败"
        return 1
    fi
    
    # 验证安装
    if [ -f "$OUTPUT_DIR/bin/ta_regtest" ]; then
        log "运行验证测试..."
        if "$OUTPUT_DIR/bin/ta_regtest"; then
            log "✅ TA-Lib 验证测试通过"
        else
            log_warning "TA-Lib 验证测试有警告"
        fi
    else
        log_warning "未找到验证工具 ta_regtest"
    fi
    
    log "✅ TA-Lib 安装完成: $OUTPUT_DIR"
    
    # 输出目录结构
    log "安装目录结构:"
    find "$OUTPUT_DIR" -type f -name "*.so" -o -name "*.dylib" -o -name "*.dll" -o -name "ta_regtest" 2>/dev/null | head -10
    
    return 0
}

# 主安装流程
log "开始 TA-Lib 安装流程..."
if install_ta_lib; then
    log "✅ TA-Lib 安装成功"
    
    # 设置GitHub Actions输出
    if [ -n "$GITHUB_OUTPUT" ]; then
        echo "ta-lib-dir=$OUTPUT_DIR" >> $GITHUB_OUTPUT
        echo "ta-lib-version=$VERSION" >> $GITHUB_OUTPUT
    fi
    
    # 设置环境变量
    echo "TA_LIB_DIR=$OUTPUT_DIR"
    echo "LD_LIBRARY_PATH=$OUTPUT_DIR/lib:\$LD_LIBRARY_PATH"
    echo "PKG_CONFIG_PATH=$OUTPUT_DIR/lib/pkgconfig:\$PKG_CONFIG_PATH"
    
    exit 0
else
    log_error "❌ TA-Lib 安装失败"
    exit 1
fi
