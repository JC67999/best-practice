# Transformer Attention Optimization

**Last Updated**: 2025-11-14
**Sources**:
- https://arxiv.org/abs/2104.09864 (Flash Attention paper)
- https://huggingface.co/docs/transformers/perf_train_gpu_one
**Relevance**: Essential for optimizing AI models in this project
**Research Trigger**: User request to "optimize transformer attention mechanism"

---

## Overview

Transformer attention mechanisms are computationally expensive (O(n²) complexity). Modern optimization techniques can reduce memory usage by 10-20x and speed up training/inference by 2-4x without accuracy loss.

---

## Key Concepts

- **Self-Attention**: Mechanism where each token attends to all other tokens
- **Multi-Head Attention**: Parallel attention mechanisms with different learned projections
- **Attention Bottleneck**: Memory and compute intensive, especially for long sequences
- **Flash Attention**: IO-aware algorithm that reduces memory access

---

## Optimization Techniques

### 1. Flash Attention

**Description**: Reorders attention computation to minimize HBM (High Bandwidth Memory) access

**Use case**: Training/inference with long sequences (>512 tokens)

**Example**:
```python
from flash_attn import flash_attn_func

# Standard attention: O(n²) memory
# attn = torch.softmax(Q @ K.T / sqrt(d), dim=-1) @ V

# Flash attention: O(n) memory, 2-4x faster
output = flash_attn_func(Q, K, V, causal=True)
```

**Benefits**:
- 2-4x faster training
- 10-20x less memory
- Exact attention (not approximation)

### 2. Multi-Query Attention (MQA)

**Description**: Share keys and values across attention heads

**Use case**: Inference optimization (faster autoregressive generation)

**Example**:
```python
class MultiQueryAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        # Multiple query heads, single key/value
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model // num_heads)  # Shared
        self.v_proj = nn.Linear(d_model, d_model // num_heads)  # Shared
```

**Benefits**:
- 1.5-2x faster inference
- Reduced KV cache size
- Minimal accuracy impact

### 3. Grouped Query Attention (GQA)

**Description**: Middle ground between MHA and MQA - group heads share K/V

**Use case**: Balance between speed and model quality

**Benefits**:
- Better than MQA for quality
- Faster than MHA for inference

---

## Best Practices

- **Training**: Use Flash Attention for sequences >512 tokens
- **Inference**: Use MQA or GQA for faster generation
- **Long context**: Consider sparse attention variants (Longformer, BigBird)
- **Hardware**: Flash Attention requires CUDA, A100/H100 GPUs optimal
- **Frameworks**: PyTorch 2.0+ has native support for some optimizations

---

## Common Pitfalls

- **Forgetting causal masking**: Flash Attention requires explicit causal flag
- **Batch size too small**: Optimizations shine with larger batches
- **Wrong hardware**: Some techniques require specific GPU architectures
- **Mixed precision issues**: Ensure FP16/BF16 compatibility

---

## Code Example: Complete Implementation

```python
import torch
import torch.nn as nn
from flash_attn import flash_attn_func

class OptimizedTransformerBlock(nn.Module):
    """Transformer block with Flash Attention optimization."""

    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads

        # Projections
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)

        self.dropout = dropout

    def forward(self, x, causal=True):
        batch_size, seq_len, _ = x.shape

        # Project to Q, K, V
        Q = self.q_proj(x).view(batch_size, seq_len, self.num_heads, self.head_dim)
        K = self.k_proj(x).view(batch_size, seq_len, self.num_heads, self.head_dim)
        V = self.v_proj(x).view(batch_size, seq_len, self.num_heads, self.head_dim)

        # Flash Attention (optimized)
        attn_output = flash_attn_func(
            Q, K, V,
            dropout_p=self.dropout if self.training else 0.0,
            causal=causal
        )

        # Reshape and project
        attn_output = attn_output.view(batch_size, seq_len, self.d_model)
        output = self.out_proj(attn_output)

        return output
```

---

## Performance Comparison

| Method | Training Speed | Memory Usage | Inference Speed | Quality |
|--------|---------------|--------------|-----------------|---------|
| Standard MHA | 1x (baseline) | 1x (baseline) | 1x (baseline) | 100% |
| Flash Attention | 2-4x faster | 10-20x less | 1.5-2x faster | 100% |
| Multi-Query (MQA) | ~1x | ~1x | 2-3x faster | ~98% |
| Grouped Query (GQA) | ~1x | ~1x | 1.5-2x faster | ~99% |

*(Based on sequences of 2048 tokens, LLaMA-7B scale)*

---

## Related Topics

- [Model Quantization](model-quantization.md) - Reduce model size
- [Inference Optimization](inference-optimization.md) - General speedup techniques
- [Memory Optimization](memory-optimization.md) - Reduce RAM/VRAM usage

---

## Resources

- **Flash Attention Paper**: https://arxiv.org/abs/2104.09864
- **Hugging Face Optimization Guide**: https://huggingface.co/docs/transformers/perf_train_gpu_one
- **PyTorch Scaled Dot Product Attention**: https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html
- **LLaMA 2 Paper (uses GQA)**: https://arxiv.org/abs/2307.09288

---

**Next Steps**:
- Implement Flash Attention in model training
- Benchmark before/after optimization
- Consider MQA for inference deployment
- Document actual results back to this knowledge base
