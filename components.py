"""
Componentes Visuais Modernos
Loading spinners, animações e widgets customizados
"""

import customtkinter as ctk
from PIL import Image, ImageDraw
import math
import threading
import time

class LoadingSpinner(ctk.CTkFrame):
    """Spinner de loading animado"""
    
    def __init__(self, parent, size=50, color="#1f77b4", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.size = size
        self.color = color
        self.running = False
        self.angle = 0
        
        # Canvas para desenhar o spinner
        self.canvas = ctk.CTkCanvas(
            self,
            width=size,
            height=size,
            bg=self._get_appearance_mode_color(),
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Arcs do spinner
        self.arcs = []
        for i in range(12):
            arc = self.canvas.create_arc(
                5, 5, size-5, size-5,
                start=i*30, extent=15,
                fill=self.color,
                outline=""
            )
            self.arcs.append(arc)
    
    def _get_appearance_mode_color(self):
        """Retorna cor de fundo baseada no tema"""
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            return "#2b2b2b"
        return "#f0f0f0"
    
    def start(self):
        """Inicia animação"""
        if not self.running:
            self.running = True
            self._animate()
    
    def stop(self):
        """Para animação"""
        self.running = False
    
    def _animate(self):
        """Loop de animação"""
        if not self.running:
            return
        
        # Rotacionar
        self.angle = (self.angle + 30) % 360
        
        # Atualizar opacidade de cada arc
        for i, arc in enumerate(self.arcs):
            angle_diff = (i * 30 - self.angle) % 360
            opacity = 1.0 - (angle_diff / 360)
            color = self._adjust_color_opacity(self.color, opacity)
            self.canvas.itemconfig(arc, fill=color)
        
        # Próximo frame
        self.after(50, self._animate)
    
    def _adjust_color_opacity(self, color, opacity):
        """Ajusta opacidade da cor"""
        # Converter hex para RGB
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # Aplicar opacidade
        bg = self._get_appearance_mode_color()
        bg_r = int(bg[1:3], 16) if bg.startswith("#") else 240
        bg_g = int(bg[3:5], 16) if bg.startswith("#") else 240
        bg_b = int(bg[5:7], 16) if bg.startswith("#") else 240
        
        r = int(r * opacity + bg_r * (1 - opacity))
        g = int(g * opacity + bg_g * (1 - opacity))
        b = int(b * opacity + bg_b * (1 - opacity))
        
        return f"#{r:02x}{g:02x}{b:02x}"


class AnimatedCard(ctk.CTkFrame):
    """Card com animação de hover"""
    
    def __init__(self, parent, hover_color=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.original_color = self.cget("fg_color")
        self.hover_color = hover_color or self._get_hover_color()
        
        # Bind de eventos
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # Bind recursivo para filhos
        self._bind_children(self)
    
    def _bind_children(self, widget):
        """Aplica bind em todos os widgets filhos"""
        for child in widget.winfo_children():
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)
            self._bind_children(child)
    
    def _get_hover_color(self):
        """Gera cor de hover automaticamente"""
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            return "#2b2b2b"
        return "#e0e0e0"
    
    def _on_enter(self, event):
        """Mouse entra no card"""
        self.configure(fg_color=self.hover_color)
    
    def _on_leave(self, event):
        """Mouse sai do card"""
        self.configure(fg_color=self.original_color)


class ProgressCircle(ctk.CTkCanvas):
    """Círculo de progresso animado"""
    
    def __init__(self, parent, size=100, thickness=10, color="#1f77b4", **kwargs):
        super().__init__(
            parent,
            width=size,
            height=size,
            highlightthickness=0,
            **kwargs
        )
        
        self.size = size
        self.thickness = thickness
        self.color = color
        self.progress = 0
        
        # Configurar fundo
        mode = ctk.get_appearance_mode()
        bg_color = "#2b2b2b" if mode == "Dark" else "#f0f0f0"
        self.configure(bg=bg_color)
        
        # Desenhar círculo de fundo
        self.bg_circle = self.create_oval(
            thickness/2, thickness/2,
            size-thickness/2, size-thickness/2,
            outline="#404040" if mode == "Dark" else "#d0d0d0",
            width=thickness
        )
        
        # Arco de progresso
        self.progress_arc = self.create_arc(
            thickness/2, thickness/2,
            size-thickness/2, size-thickness/2,
            start=90, extent=0,
            outline=color,
            width=thickness,
            style="arc"
        )
        
        # Texto central
        self.text = self.create_text(
            size/2, size/2,
            text="0%",
            font=("Arial", int(size/5), "bold"),
            fill=color
        )
    
    def set_progress(self, value, animate=True):
        """Define progresso (0-100)"""
        value = max(0, min(100, value))
        
        if animate:
            self._animate_to(value)
        else:
            self.progress = value
            self._update_display()
    
    def _animate_to(self, target):
        """Anima até o valor alvo"""
        if abs(self.progress - target) < 1:
            self.progress = target
            self._update_display()
            return
        
        # Incremento suave
        diff = target - self.progress
        self.progress += diff * 0.1
        self._update_display()
        
        # Próximo frame
        self.after(20, lambda: self._animate_to(target))
    
    def _update_display(self):
        """Atualiza visualização"""
        # Atualizar arco
        extent = -(self.progress / 100 * 360)
        self.itemconfig(self.progress_arc, extent=extent)
        
        # Atualizar texto
        self.itemconfig(self.text, text=f"{int(self.progress)}%")


class NotificationToast(ctk.CTkToplevel):
    """Toast de notificação estilo material"""
    
    def __init__(self, parent, message, tipo="info", duration=3000):
        super().__init__(parent)
        
        # Configurar janela
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        
        # Cores por tipo
        cores = {
            "info": "#1f77b4",
            "success": "#2ca02c",
            "warning": "#ff7f0e",
            "error": "#d62728"
        }
        
        icones = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        cor = cores.get(tipo, "#1f77b4")
        icone = icones.get(tipo, "ℹ️")
        
        # Frame principal
        frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color=cor
        )
        frame.pack(padx=2, pady=2)
        
        # Conteúdo
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(padx=15, pady=10)
        
        ctk.CTkLabel(
            content_frame,
            text=f"{icone} {message}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        ).pack()
        
        # Posicionar no canto superior direito
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        x = screen_width - width - 20
        y = 20
        self.geometry(f"+{x}+{y}")
        
        # Auto-destruir após duração
        self.after(duration, self._fade_out)
    
    def _fade_out(self):
        """Animação de fade out"""
        alpha = self.attributes('-alpha')
        if alpha > 0:
            self.attributes('-alpha', alpha - 0.1)
            self.after(50, self._fade_out)
        else:
            self.destroy()


class IconButton(ctk.CTkButton):
    """Botão com ícone grande e hover effect"""
    
    def __init__(self, parent, icon, text="", command=None, **kwargs):
        super().__init__(
            parent,
            text=f"{icon}\n{text}" if text else icon,
            command=command,
            corner_radius=15,
            font=ctk.CTkFont(size=16),
            **kwargs
        )
        
        # Efeito hover
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.original_size = self.cget("font").cget("size")
    
    def _on_enter(self, event):
        """Aumenta tamanho no hover"""
        font = self.cget("font")
        font.configure(size=self.original_size + 2)
    
    def _on_leave(self, event):
        """Volta ao tamanho normal"""
        font = self.cget("font")
        font.configure(size=self.original_size)


class ConfirmDialog(ctk.CTkToplevel):
    """Diálogo de confirmação moderno"""
    
    def __init__(self, parent, title, message, on_confirm=None, on_cancel=None):
        super().__init__(parent)
        
        self.result = None
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        
        # Configurar janela
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()
        
        # Centralizar
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Mensagem
        label = ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        label.pack(pady=30, padx=20)
        
        # Botões
        frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        frame_btns.pack(pady=20)
        
        btn_cancel = ctk.CTkButton(
            frame_btns,
            text="❌ Cancelar",
            command=self._cancel,
            fg_color="#6c757d",
            hover_color="#5a6268",
            width=150
        )
        btn_cancel.pack(side="left", padx=10)
        
        btn_confirm = ctk.CTkButton(
            frame_btns,
            text="✅ Confirmar",
            command=self._confirm,
            fg_color="#2ca02c",
            hover_color="#28a745",
            width=150
        )
        btn_confirm.pack(side="left", padx=10)
        
        # Enter = confirmar, Esc = cancelar
        self.bind("<Return>", lambda e: self._confirm())
        self.bind("<Escape>", lambda e: self._cancel())
    
    def _confirm(self):
        """Confirma ação"""
        self.result = True
        if self.on_confirm:
            self.on_confirm()
        self.destroy()
    
    def _cancel(self):
        """Cancela ação"""
        self.result = False
        if self.on_cancel:
            self.on_cancel()
        self.destroy()
    
    def get_result(self):
        """Retorna resultado"""
        self.wait_window()
        return self.result


class SearchBar(ctk.CTkFrame):
    """Barra de busca moderna com ícone"""
    
    def __init__(self, parent, placeholder="Buscar...", on_search=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.on_search = on_search
        
        # Frame com borda
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="x")
        
        # Ícone de busca
        label_icon = ctk.CTkLabel(
            frame,
            text="🔍",
            font=ctk.CTkFont(size=16)
        )
        label_icon.pack(side="left", padx=10)
        
        # Entry
        self.entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            border_width=0,
            fg_color="transparent"
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Bind de eventos
        self.entry.bind("<Return>", lambda e: self._do_search())
        self.entry.bind("<KeyRelease>", lambda e: self._on_key_release())
    
    def _do_search(self):
        """Executa busca"""
        if self.on_search:
            self.on_search(self.entry.get())
    
    def _on_key_release(self):
        """Busca em tempo real"""
        if self.on_search:
            self.after(300, self._do_search)
    
    def get(self):
        """Retorna valor do entry"""
        return self.entry.get()
    
    def set(self, value):
        """Define valor do entry"""
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
    
    def clear(self):
        """Limpa entry"""
        self.entry.delete(0, "end")


def show_toast(parent, message, tipo="info", duration=3000):
    """Função helper para mostrar toast"""
    NotificationToast(parent, message, tipo, duration)


def show_loading(parent, message="Carregando..."):
    """Mostra overlay de loading"""
    overlay = ctk.CTkFrame(parent, fg_color=("#f0f0f0", "#2b2b2b"))
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    spinner = LoadingSpinner(overlay, size=60)
    spinner.place(relx=0.5, rely=0.45, anchor="center")
    spinner.start()
    
    label = ctk.CTkLabel(
        overlay,
        text=message,
        font=ctk.CTkFont(size=14)
    )
    label.place(relx=0.5, rely=0.55, anchor="center")
    
    return overlay, spinner


def hide_loading(overlay, spinner):
    """Esconde overlay de loading"""
    spinner.stop()
    overlay.destroy()
