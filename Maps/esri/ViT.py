# Patchify
class PatchEmbed(nn.Module):
    def __init__(self, image_size, patch_size, in_channels, embed_dim):
        """
        image_size: 图片尺寸 (H, W)
        patch_size: patch 尺寸 (H, W)
        in_channels: 输入通道数 C
        embed_dim: 嵌入维度
        """
        super(PatchEmbed, self).__init__()
        # 验证可分
        image_h, image_w = image_size
        patch_h, patch_w = patch_size
        assert image_h % patch_h == 0 and image_w % patch_w == 0, 'image dimensions must be divisible by the patch size'

        self.image_size = image_size
        self.patch_size = patch_size
        self.num_patches = (image_h // patch_h) * (image_w // patch_w)
        self.patch_dim = in_channels * patch_h * patch_w
        self.proj = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size)
    
    def forward(self, x):
        x = self.proj(x)
        x = x.flatten(2).transpose(1, 2)
        return x

## 定义模型 ViT
class ViT(nn.Module):
    def __init__(self, image_size, patch_size, in_channels, embed_dim, num_classes, depth, heads, mlp_dim):
        super(ViT, self).__init__()
        self.patch_embed = PatchEmbed(image_size, patch_size, in_channels, embed_dim)
        num_patches = self.patch_embed.num_patches

        self.patch_conv = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size)
        self.cls_token = nn.Parameter(torch.randn(1, 1, embed_dim))
        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, embed_dim))
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(embed_dim, heads, mlp_dim, batch_first=True),
            depth
        )

        self.mlp_head = nn.Sequential(
            nn.LayerNorm(embed_dim),
            nn.Linear(embed_dim, num_classes)
        )
    
    def forward(self, x):
        batch_size = x.shape[0]
        x = self.patch_conv(x)
        x = x.flatten(2).transpose(1, 2)
        # print(x.shape, self.cls_token.shape, self.pos_embedding.shape)
        x = torch.cat([self.cls_token.expand(batch_size, -1, -1), x], dim=1)
        x += self.pos_embedding
        x = self.transformer(x)
        x = x.mean(dim=1)
        return self.mlp_head(x)