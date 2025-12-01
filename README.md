# Solana Token Transfer

一个使用 Python 在 Solana 区块链上转账 SOL 和 USDC 代币的工具。

## 功能特性

- ✅ 转账 SOL 代币
- ✅ 转账 USDC (SPL Token)
- ✅ 使用 UV 管理 Python 环境
- ✅ 私钥安全存储在 `.env` 文件中

## 前置要求

- Python 3.9 或更高版本
- UV (Python 包管理器)

## 安装 UV

如果还没有安装 UV,可以使用以下命令安装:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或者使用 pip
pip install uv
```

## 项目设置

### 1. 克隆或进入项目目录

```bash
cd /Users/scottliyq/go/quant/sol_test
```

### 2. 创建虚拟环境并安装依赖

```bash
# 使用 UV 同步依赖
uv sync
```

### 3. 配置环境变量

复制示例环境变量文件:

```bash
cp .env.example .env
```

编辑 `.env` 文件,填入您的配置:

```env
# Solana 私钥 (Base58 编码)
PRIVATE_KEY=your_base58_private_key_here

# Solana RPC 端点
# 主网: https://api.mainnet-beta.solana.com
# 测试网: https://api.testnet.solana.com
# 开发网: https://api.devnet.solana.com
RPC_URL=https://api.mainnet-beta.solana.com


```

**⚠️ 安全提醒**: 
- 不要将 `.env` 文件提交到版本控制系统
- 确保私钥安全,不要泄露给他人
- 建议先在测试网测试

## 使用方法

```bash
# 转账 SOL
uv run python main.py sol <接收地址> <数量>

# 转账 USDC
uv run python main.py usdc <接收地址> <数量>
```

### 使用示例

```bash
# 转账 0.1 SOL
uv run python main.py sol 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 0.1

# 转账 10 USDC
uv run python main.py usdc 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 10
```

## 项目结构

```
sol_test/
├── main.py              # 主程序 (包含所有转账功能)
├── pyproject.toml       # 项目配置和依赖
├── .env                 # 环境变量 (需要自己创建)
├── .env.example         # 环境变量示例
├── .gitignore          # Git 忽略文件
└── README.md           # 项目说明文档
```

## 依赖项

- `solana>=0.34.0` - Solana Python SDK
- `solders>=0.21.0` - Solana Rust 绑定
- `anchorpy>=0.19.0` - Anchor 框架 Python 绑定
- `python-dotenv>=1.0.0` - 环境变量管理

## 注意事项

1. **网络选择**: 默认使用主网,测试时请修改 `.env` 中的 `RPC_URL` 为测试网或开发网
2. **Gas 费用**: 转账需要支付网络 Gas 费用,确保账户有足够的 SOL
3. **USDC 账户**: 接收方必须有对应的 USDC 关联代币账户 (Associated Token Account)
4. **私钥格式**: 私钥应为 Base58 编码格式

## 获取测试 SOL

如果在开发网测试,可以使用水龙头获取测试 SOL:

```bash
solana airdrop 1 <你的地址> --url https://api.devnet.solana.com
```

## 故障排除

### 问题: 无法解析导入

如果遇到导入错误,确保已安装所有依赖:

```bash
uv sync
```

### 问题: 私钥格式错误

确保私钥是 Base58 编码格式。如果您的私钥是 JSON 数组格式,需要转换为 Base58。

### 问题: 交易失败

1. 检查账户余额是否足够
2. 验证接收地址是否正确
3. 检查网络连接和 RPC 端点是否可用

## 查看交易

交易成功后会输出交易签名和浏览器链接,可以在以下浏览器查看:

- Solscan: https://solscan.io/tx/{signature}
- Solana Explorer: https://explorer.solana.com/tx/{signature}

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request!
